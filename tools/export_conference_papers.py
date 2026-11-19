"""Export verified conference paper records as one static JSON file per edition."""

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.parse import urlsplit

from export_conference_archive import load_json


SITE_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ARCHIVE = SITE_ROOT / "_data" / "conference_archive.json"
DEFAULT_OUTPUT = SITE_ROOT / "assets" / "conference-papers"
PAPER_URL_FIELDS = ("official_record_url", "doi_url", "publisher_record_url")
EDITION_ID = re.compile(r"[a-zA-Z0-9]+(?:-[a-zA-Z0-9]+)+")
TITLE_SCRIPT = re.compile(r"\$?<(?P<kind>sub|sup)>(?P<text>[^<>]+)</(?P=kind)>\$?", re.IGNORECASE)
TITLE_SCRIPTS = {
    "sub": str.maketrans("0123456789k", "₀₁₂₃₄₅₆₇₈₉ₖ"),
    "sup": str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹"),
}
NONRESEARCH_KINDS = {"front_matter", "supplementary_material", "retraction_notice", "erratum"}


def public_url(value):
    if not value or any(character.isspace() or ord(character) < 32 for character in value):
        return None
    parts = urlsplit(value)
    if (
        parts.scheme not in {"http", "https"}
        or not parts.hostname
        or parts.username is not None
        or parts.password is not None
        or not re.fullmatch(r"[a-z0-9-]+(?:\.[a-z0-9-]+)+", parts.hostname)
        or parts.hostname.endswith((".localhost", ".local", ".internal"))
        or parts.hostname.replace(".", "").isdigit()
    ):
        return None
    return value


def display_title(value):
    def script_text(match):
        return match["text"].strip().translate(TITLE_SCRIPTS[match["kind"].lower()])

    title = TITLE_SCRIPT.sub(script_text, value)
    return " ".join(re.sub(r"</?u>", "", title, flags=re.IGNORECASE).split())


def read_source_records(tracker, entry, edition):
    pointer = load_json(tracker / entry["verified_pointer"])
    delivery_root = (tracker / "03_交付物").resolve()
    report = (tracker / pointer["report_path"]).resolve()
    source = (tracker / pointer.get("papers_path", report / "papers.jsonl")).resolve()
    report.relative_to(delivery_root)
    source.relative_to(report)

    expected_prefix = f"{entry['series_id']}-{entry['year']}-"
    if entry["year"] != edition["year"] or not entry["instance"].startswith(expected_prefix):
        raise ValueError(f"Mismatched archive and registry record: {entry['instance']}")
    records = []
    seen = set()
    with source.open(encoding="utf-8") as lines:
        for line_number, line in enumerate(lines, 1):
            record = json.loads(line)
            record_id = record["record_id"]
            # Older combined catalogues include several tracks for the same meeting.
            if (
                not record_id or record_id in seen
                or record["series_id"] != entry["series_id"]
                or record["edition_year"] != entry["year"]
                or not record["edition_id"].startswith(expected_prefix)
            ):
                raise ValueError(f"Invalid record identity in {entry['instance']} at row {line_number}")
            seen.add(record_id)
            records.append(record)

    with_abstract = sum(bool((record["abstract"] or "").strip()) for record in records)
    if len(records) != edition["records"] or with_abstract != edition["abstracts"]:
        raise ValueError(f"Paper or abstract count does not match archive for {entry['instance']}")
    return records


def export_edition(records, edition, include_abstracts):
    # Collection-level links belong in the archive list, not on individual records.
    collection_urls = {source["url"] for source in edition["sources"]}
    paper_urls = [
        dict.fromkeys(
            url for field in PAPER_URL_FIELDS
            if (url := public_url(record.get(field))) and url not in collection_urls
        )
        for record in records
    ]
    url_usage = Counter(url for urls in paper_urls for url in urls)
    papers = []
    for record, urls in zip(records, paper_urls):
        title = display_title(record["title"])
        if not title:
            raise ValueError(f"Untitled record in {edition['id']}")
        authors = ", ".join(author.strip() for author in record["authors"] if author.strip())
        url = next((url for url in urls if url_usage[url] == 1), None)

        status = None
        if record.get("publication_status") == "retracted":
            status = "retracted"
        elif record.get("record_kind") in NONRESEARCH_KINDS:
            status = "nonresearch"

        paper = [title, authors, url]
        if include_abstracts or status:
            abstract = (record["abstract"] or "").strip() if include_abstracts else None
            paper.append(abstract or None)
        if status:
            paper.append(status)
        papers.append(paper)
    return {"edition": edition["id"], "papers": papers}


def prune_stale_shards(output_dir, current_ids):
    for file in output_dir.glob("*.json"):
        if file.stem in current_ids or not EDITION_ID.fullmatch(file.stem) or not file.is_file() or file.is_symlink():
            continue
        try:
            shard = load_json(file)
        except (OSError, ValueError):
            continue
        if isinstance(shard, dict) and shard.keys() == {"edition", "papers"}:
            if shard["edition"] == file.stem and isinstance(shard["papers"], list):
                file.unlink()


def export_papers(tracker, archive_path, output_dir, include_abstracts):
    registry = load_json(tracker / "配置" / "conferences.json")
    if registry.get("schema_version") != 2:
        raise ValueError("Unsupported conference registry schema")
    entries = {entry["instance"]: entry for entry in registry["conferences"]}
    if len(entries) != len(registry["conferences"]):
        raise ValueError("Conference registry contains duplicate instances")
    archive = load_json(archive_path)
    editions = archive["editions"]
    ids = {edition["id"] for edition in editions}
    if len(ids) != len(editions) or not all(EDITION_ID.fullmatch(key) for key in ids):
        raise ValueError("Archive contains duplicated or invalid edition IDs")
    if missing := ids.difference(entries):
        raise ValueError(f"Archive editions missing from the tracker: {', '.join(sorted(missing))}")

    output_dir.parent.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(prefix="conference-papers-", dir=output_dir.parent) as temp:
        staged = Path(temp)
        for edition in editions:
            key = edition["id"]
            records = read_source_records(tracker, entries[key], edition)
            shard = export_edition(records, edition, include_abstracts)
            with (staged / f"{key}.json").open("w", encoding="utf-8") as handle:
                json.dump(shard, handle, ensure_ascii=False, separators=(",", ":"))
                handle.write("\n")

        output_dir.mkdir(exist_ok=True)
        for file in staged.iterdir():
            file.replace(output_dir / file.name)
        prune_stale_shards(output_dir, ids)
    print(f"Exported {sum(edition['records'] for edition in editions):,} records across {len(editions)} editions.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tracker", type=Path, help="Root of the conference tracking project")
    parser.add_argument("--archive", type=Path, default=DEFAULT_ARCHIVE, help="Generated archive index")
    parser.add_argument("--output-dir", type=Path, help="Directory for per-edition JSON files")
    parser.add_argument("--include-abstracts", action="store_true", help="Include stored abstracts for a local preview")
    args = parser.parse_args()
    output_dir = (args.output_dir or DEFAULT_OUTPUT).resolve()
    tracker = args.tracker.resolve()
    if output_dir.is_relative_to(tracker):
        parser.error("The export directory must be outside the source tracking project")
    if args.include_abstracts and (not args.output_dir or output_dir.is_relative_to(SITE_ROOT)):
        parser.error("--include-abstracts requires --output-dir outside the website repository")
    export_papers(tracker, args.archive, output_dir, args.include_abstracts)


if __name__ == "__main__":
    main()
