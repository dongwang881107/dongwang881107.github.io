"""Export a browsable index from the conference tracker's verified catalogues."""

import argparse
import json
from datetime import date
from pathlib import Path
from tempfile import NamedTemporaryFile
from urllib.parse import urlsplit


# Dates confirmed by the organisers or proceedings publisher. Use these when
# the tracker has a verified paper catalogue but no date in its watchlist.
HISTORICAL_DATES = {
    "AISTATS-2026-main": ("2026-05-02", "2026-05-05", "https://virtual.aistats.org/Conferences/2026"),
    "COLT-2026-main": ("2026-06-29", "2026-07-03", "https://learningtheory.org/colt2026/"),
    "ICASSP-2026-main": ("2026-05-04", "2026-05-08", "https://2026.ieeeicassp.org/event/about-conference/"),
    "ICIP-2026-main": ("2026-09-13", "2026-09-17", "https://2026.ieeeicip.org/important-dates/"),
    "ICPR-2024-main": ("2024-12-01", "2024-12-05", "https://link.springer.com/conference/icpr"),
    "ICPR-2026-main": ("2026-08-17", "2026-08-22", "https://icpr2026.org/program.html"),
    "MICCAI-2022-main": ("2022-09-18", "2022-09-22", "https://link.springer.com/book/10.1007/978-3-031-16431-6"),
    "MICCAI-2023-main": ("2023-10-08", "2023-10-12", "https://link.springer.com/book/10.1007/978-3-031-43907-0"),
    "UAI-2026-main": ("2026-08-18", "2026-08-20", "https://auai.org/uai2026/"),
}

PROGRAMME_PAGES = {
    "CVPR-2023-main": "https://cvpr.thecvf.com/virtual/2023/papers.html",
    "CVPR-2024-main": "https://cvpr.thecvf.com/virtual/2024/papers.html",
    "ICLR-2022-main": "https://iclr.cc/virtual/2022/papers.html",
    "ICLR-2023-main": "https://iclr.cc/virtual/2023/papers.html",
}

# Older tracker configs do not always carry a machine-readable collection scope.
PUBLISHER_METADATA = {
    "AAAI-2026-proceedings",
    "ACM-MM-2022-proceedings",
    "ACM-MM-2023-proceedings",
    "ICCV-2019-proceedings",
    "ICCV-2021-proceedings",
    "ICASSP-2026-main",
    "ICIP-2026-main",
    "ICME-2025-main",
    "BIBM-2025-main",
}
ACCEPTED_CATALOGUES = {"ACM-MM-2025-regular", "ECCV-2026-main"}
PROCEEDINGS_PAGES = {
    "ICPR-2024-main": "https://link.springer.com/book/10.1007/978-3-031-78107-0",
    "MICCAI-2022-main": "https://link.springer.com/book/10.1007/978-3-031-16431-6",
    "MICCAI-2023-main": "https://link.springer.com/book/10.1007/978-3-031-43907-0",
    "MICCAI-2024-main": "https://link.springer.com/book/10.1007/978-3-031-72378-0",
}
CONFERENCE_PAGES = {
    "AAAI-2025-proceedings": "https://aaai.org/conference/aaai/aaai-25/",
    "MICCAI-2025-main": "https://conferences.miccai.org/2025/files/downloads/MICCAI2025-Program-Book.pdf",
}


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def check_url(url):
    parts = urlsplit(url)
    if parts.scheme != "https" or not parts.hostname or parts.username or parts.password or any(map(str.isspace, url)):
        raise ValueError("Archive source must be an HTTPS URL without credentials or whitespace")
    return url


def watchlist_dates(watchlist):
    public_sources = {entry["source_id"]: entry["url"] for entry in watchlist["sources"] if entry["status"] == "ok"}
    dates = {}
    for edition in watchlist["editions"]:
        if edition["year_confirmation"] != "confirmed":
            continue
        candidates = {
            (
                event["start_date"],
                event.get("end_date") or event["start_date"],
                public_sources[event["source_id"]],
            )
            for event in edition["events"]
            if event["event_type"] == "conference"
            and event["confidence"] == "verified"
            and event["source_id"] in public_sources
        }
        if len(candidates) == 1:
            dates[edition["edition_id"]] = candidates.pop()
    return dates


def edition_dates(config, dates):
    instance = config["edition_id"]
    if instance in dates:
        return dates[instance]
    candidates = {
        (event["start_date"], event.get("end_date") or event["start_date"], event["source_url"])
        for event in config["events"]
        if event["event_type"] == "conference" and event.get("source_url")
    }
    if len(candidates) == 1:
        return candidates.pop()
    return HISTORICAL_DATES.get(instance)


def archive_sources(config, verification, date_source):
    instance, series, links = config["edition_id"], config["series_id"], config["sources"]
    proceedings = links.get("cvf_index") or links.get("official_proceedings") or links.get("index")
    program = PROGRAMME_PAGES.get(instance) or links.get("program_home")
    catalog = links.get("accepted") or links.get("accepted_papers")
    source_pairs = []
    if program:
        coverage = "program"
        source_pairs.append(("program", program))
        if series == "ICLR":
            proceedings = None  # The shared FAQ is not this edition's proceedings.
    elif (
        instance in PUBLISHER_METADATA
        or verification.get("official_toc_reconciled") is False
        or verification.get("publisher_deposit_count")
        or (proceedings and urlsplit(proceedings).hostname == "api.crossref.org")
    ):
        coverage = "metadata"
        registration = links.get("crossref") or links.get("crossref_parent") or links.get("ieee_proceedings")
        source_pairs.append(("metadata", registration or proceedings))
    elif series == "MICCAI" or instance in ACCEPTED_CATALOGUES:
        coverage = "catalog"
        source_pairs.append(("catalog", catalog or links.get("index") or proceedings))
        if series == "MICCAI":
            proceedings = links.get("proceedings") or links.get("springer_book")
    else:
        coverage = "proceedings"

    official_volume = verification.get("official_volume_url") or PROCEEDINGS_PAGES.get(instance) or proceedings
    homepage = CONFERENCE_PAGES.get(instance) or date_source or links.get("conference_home") or links.get("home") or links.get("official_home")
    source_pairs.extend((("proceedings", official_volume), ("conference", homepage)))
    sources = []
    seen = set()
    for kind, url in source_pairs:
        if url and url not in seen:
            sources.append({"kind": kind, "url": check_url(url)})
            seen.add(url)
    if not sources:
        raise ValueError(f"Archive edition has no public source: {instance}")
    return coverage, sources


def read_catalogue(root, entry):
    pointer = load_json(root / entry["verified_pointer"])
    delivery = (root / pointer["report_path"]).resolve()
    delivery.relative_to((root / "03_交付物").resolve())
    verification = load_json(delivery / "verification.json")
    config = load_json(root / entry["config"])
    instance = entry["instance"]
    if (config["series_id"], config["edition_year"], config["edition_id"]) != (entry["series_id"], entry["year"], instance):
        raise ValueError(f"Catalogue and config identity mismatch: {instance}")
    if verification.get("edition_id", instance) != instance:
        raise ValueError(f"Catalogue and verification identity mismatch: {instance}")
    return config, verification


def export_archive(root, as_of=None):
    watchlist = load_json(root / "配置" / "watchlist.json")
    registry = load_json(root / "配置" / "conferences.json")
    if watchlist.get("schema_version") != 1 or registry.get("schema_version") != 2:
        raise ValueError("Unsupported watchlist or catalogue schema")
    profiles = load_json(root / "配置" / "conference_profiles.json")["entries"]
    as_of = as_of or date.fromisoformat(watchlist["verified_as_of"])
    series = {entry["series_id"]: entry for entry in watchlist["series"]}
    dates = watchlist_dates(watchlist)
    editions = []
    seen = set()
    for entry in registry["conferences"]:
        sid, year, instance = entry["series_id"], entry["year"], entry["instance"]
        if year > as_of.year:
            continue
        if instance in seen:
            raise ValueError(f"Duplicate catalogue instance: {instance}")
        seen.add(instance)

        config, verification = read_catalogue(root, entry)
        timing = edition_dates(config, dates)
        if timing:
            start, end, date_source = timing
            last_day = date.fromisoformat(end)
            if last_day < date.fromisoformat(start):
                raise ValueError(f"Conference ends before it starts: {instance}")
            if last_day >= as_of:
                continue
        else:
            # With a year alone, a current-year meeting could still be upcoming.
            if year == as_of.year:
                continue
            date_source = None

        records = verification.get("paper_count", verification.get("normalized_count"))
        abstracts = verification["abstract_count"]
        nonresearch = verification.get("abstract_not_applicable_count", 0)
        pending = records - abstracts - nonresearch
        if min(records, abstracts, nonresearch, pending) < 0 or verification.get("abstracts_pending", pending) != pending:
            raise ValueError(f"Inconsistent catalogue counts: {instance}")

        coverage, sources = archive_sources(config, verification, date_source)
        display_name = series[sid]["display_name"]
        item = {
            "id": instance,
            "series": display_name,
            "title": profiles.get(sid, {}).get("full_name") or display_name,
            "year": year,
            "coverage": coverage,
            "records": records,
            "abstracts": abstracts,
        }
        ccf = series[sid].get("ccf_class")
        if ccf in {"A", "B", "C"}:
            item["ccf"] = ccf
        if timing:
            item.update(start=start, end=end)
        if verification.get("volume_publication_verified"):
            item["matched"] = verification["doi_enrichment_count"]
        elif instance == "ECCV-2026-main":
            item["matched"] = verification["official_publication_count"]
        elif verification.get("publication_exact_title_author_matches") is not None:
            item["matched"] = (
                verification["publication_exact_title_author_matches"]
                + verification.get("publication_manually_reconciled_title_variants", 0)
            )
        item["sources"] = sources
        editions.append(item)

    editions.sort(key=lambda item: (-item["year"], item["series"].casefold(), item["id"]))
    return {
        "as_of": as_of.isoformat(),
        "edition_count": len(editions),
        "series_count": len({item["series"] for item in editions}),
        "record_count": sum(item["records"] for item in editions),
        "abstract_count": sum(item["abstracts"] for item in editions),
        "editions": editions,
    }


def main():
    output_path = Path(__file__).resolve().parents[1] / "_data" / "conference_archive.json"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tracker", type=Path, help="Root of the conference tracking project")
    parser.add_argument("--as-of", type=date.fromisoformat, help="Archive cutoff; defaults to the watchlist verification date")
    parser.add_argument("--output", type=Path, default=output_path)
    args = parser.parse_args()
    data = export_archive(args.tracker, args.as_of)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = None
    try:
        with NamedTemporaryFile(mode="w", dir=args.output.parent, encoding="utf-8", delete=False) as out:
            temporary_path = Path(out.name)
            json.dump(data, out, ensure_ascii=False, indent=2)
            out.write("\n")
        temporary_path.chmod(0o644)
        temporary_path.replace(args.output)
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)
    print(f"{data['edition_count']} editions, {data['series_count']} series, {data['record_count']} records")


if __name__ == "__main__":
    main()
