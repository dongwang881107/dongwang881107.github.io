"""Export a public schedule snapshot from the local conference watchlist."""

import argparse
import json
from collections import Counter
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path
from tempfile import NamedTemporaryFile
from urllib.parse import urlsplit
from zoneinfo import ZoneInfo


BEIJING = ZoneInfo("Asia/Shanghai")
AOE = timezone(timedelta(hours=-12))
EVENTS = {
    "registration_deadline": ("submission", "Paper registration deadline"),
    "abstract_deadline": ("submission", "Abstract deadline"),
    "paper_deadline": ("submission", "Full paper deadline"),
    "supplement_deadline": ("submission", "Supplementary material deadline"),
    "decision": ("decision", "Acceptance notification"),
    "early_acceptance": ("decision", "Early acceptance notification"),
    "conference": ("conference", "Conference"),
    "conference_session": ("conference", "Conference session"),
}
ENGLISH_LABELS = {
    "Full论文摘要注册截止": "Full paper abstract registration deadline",
    "Full论文全文截止": "Full paper submission deadline",
    "全文及附录截止": "Full paper and appendix deadline",
    "Regular/Special Session全文截止": "Regular / Special Session paper deadline",
    "Regular/Special Session全文截止（6页含参考文献）": "Regular / Special Session paper deadline (6 pages including references)",
    "最终结果": "Final decision",
    "Regular论文录用通知": "Regular paper acceptance notification",
    "Regular录用通知": "Regular paper acceptance notification",
    "作者通知最晚日期": "Latest author notification date",
    "主会": "Main conference",
    "主会会期": "Main conference",
    "会议整体会期": "Full conference dates",
    "会议整体会期（当届官网）": "Full conference dates",
    "主会技术场次": "Main technical sessions",
    "Sydney整体活动": "Sydney programme",
    "Sydney主会": "Sydney main conference",
    "Atlanta卫星整体活动": "Atlanta satellite programme",
    "Paris卫星整体活动": "Paris satellite programme",
}


def official_url(source):
    url = source["url"]
    parsed = urlsplit(url)
    if parsed.scheme not in {"https", "http"} or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError(f"Invalid public URL for {source['source_id']}")
    return url


def timing(event):
    """Return display fields and the interval's Beijing calendar boundaries."""
    source_zone = event.get("source_timezone")
    if event.get("iso_time"):
        original = datetime.fromisoformat(event["iso_time"])
        if original.utcoffset() is None:
            raise ValueError(f"Exact time has no offset: {event['iso_time']}")
        local = original.astimezone(BEIJING)
        local_day = local.date()
        original_zone = source_zone or original.strftime("%z")
        return {
            "start": local_day.isoformat(),
            "clock": local.strftime("%H:%M"),
            "timezone": BEIJING.key,
            "original": {
                "date": original.date().isoformat(),
                "clock": original.strftime("%H:%M"),
                "timezone": original_zone,
            },
        }, local_day, local_day

    start = date.fromisoformat(event["start_date"])
    end = date.fromisoformat(event.get("end_date") or event["start_date"])
    if end < start:
        raise ValueError("Conference event ends before it starts")
    fields = {"start": start.isoformat()}
    if event.get("end_date"):
        fields["end"] = end.isoformat()
    if not source_zone:
        return fields, start, end

    fields["timezone"] = source_zone
    zone = AOE if source_zone == "UTC-12:00" else ZoneInfo(source_zone)
    first = datetime.combine(start, time.min, zone).astimezone(BEIJING).date()
    last = datetime.combine(end, time.max, zone).astimezone(BEIJING).date()
    return fields, first, last


def checked_on(event, edition, source):
    if event.get("date_checked_as_of"):
        return event["date_checked_as_of"]
    latest = source.get("latest_check") or {}
    if latest.get("status") == "ok" and latest.get("checked_as_of"):
        return latest["checked_as_of"]
    if source.get("observed_at"):
        return datetime.fromisoformat(source["observed_at"]).astimezone(BEIJING).date().isoformat()
    return edition.get("verified_as_of")


def pending_row(conference, source, *, unannounced=False):
    if unannounced:
        zh = "下一届日程待官方公布。"
        en = "The next edition's schedule has yet to be announced."
    else:
        zh = "官网日程暂定，等待确认。"
        en = "The dates on the official site are tentative."
    return {"conference": conference, "label_zh": zh, "label_en": en, "source": official_url(source)}


def export_schedule(watchlist, as_of, horizon_days):
    if watchlist.get("schema_version") != 1:
        raise ValueError("Unsupported watchlist schema")
    through = as_of + timedelta(days=horizon_days)
    series = {row["series_id"]: row for row in watchlist["series"] if row["tracked"]}
    sources = {row["source_id"]: row for row in watchlist["sources"]}
    schedule = []
    pending = {}
    seen = set()
    for edition in watchlist["editions"]:
        conference_series = series.get(edition["series_id"])
        if not conference_series:
            continue
        name = conference_series["display_name"]
        if edition["year_confirmation"] != "confirmed":
            if edition["edition_id"] == conference_series["primary_edition_id"]:
                home = sources[edition["official_home_source_id"]]
                pending[name] = pending_row(name, home, unannounced=True)
            continue
        conference = f"{name} {edition['year']}"
        if edition["track"] != "Main Conference":
            conference += f" · {edition['track']}"

        for event in edition["events"]:
            spec = EVENTS.get(event["event_type"])
            if not spec:
                continue
            dates, start, end = timing(event)
            if end < as_of or start > through:
                continue
            source = sources[event["source_id"]]
            if source["status"] != "ok":
                raise ValueError(f"Schedule event has no usable source: {event['source_id']}")
            if event["confidence"] == "tentative":
                pending.setdefault(conference, pending_row(conference, source))
                continue
            if event["confidence"] != "verified" or not event["reminder_eligible"]:
                continue

            kind, default_label = spec
            label = event["label"]
            key = (conference, kind, label, dates["start"], dates.get("end"), dates.get("clock"))
            if key in seen:
                continue
            seen.add(key)
            row = {
                "kind": kind,
                "conference": conference,
                "label_zh": label,
                "label_en": ENGLISH_LABELS.get(label, default_label),
                **dates,
                "source": official_url(source),
            }
            ccf = conference_series.get("ccf_class")
            if ccf in {"A", "B", "C"}:
                row["ccf"] = ccf
            checked = checked_on(event, edition, source)
            if checked:
                row["checked"] = date.fromisoformat(checked).isoformat()
            schedule.append((max(start, as_of), dates.get("clock", ""), conference, kind, row))

    schedule.sort(key=lambda item: item[:-1])
    return {
        "as_of": as_of.isoformat(),
        "through": through.isoformat(),
        "verified_as_of": date.fromisoformat(watchlist["verified_as_of"]).isoformat(),
        "horizon_days": horizon_days,
        "events": [item[-1] for item in schedule],
        "pending": [pending[name] for name in sorted(pending)],
    }


def main():
    output_path = Path(__file__).resolve().parents[1] / "_data" / "conference_schedule.json"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("watchlist", type=Path, help="Path to the tracking project's watchlist.json")
    parser.add_argument("--as-of", type=date.fromisoformat, help="Window start (defaults to the snapshot verification date)")
    parser.add_argument("--days", type=int, default=180, help="Days after the window start to include")
    parser.add_argument("--output", type=Path, default=output_path)
    args = parser.parse_args()
    if args.days < 1:
        parser.error("--days must be positive")

    watchlist = json.loads(args.watchlist.read_text(encoding="utf-8"))
    as_of = args.as_of or date.fromisoformat(watchlist["verified_as_of"])
    data = export_schedule(watchlist, as_of, args.days)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = None
    try:
        with NamedTemporaryFile(mode="w", dir=args.output.parent, encoding="utf-8", delete=False) as out:
            temporary_path = Path(out.name)
            json.dump(data, out, ensure_ascii=False, indent=2)
            out.write("\n")
        temporary_path.replace(args.output)
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)
    print(Counter(event["kind"] for event in data["events"]), f"+ {len(data['pending'])} pending")


if __name__ == "__main__":
    main()
