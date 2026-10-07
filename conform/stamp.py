"""stamp: a channel post's time is READ, never typed (the reviewer 2026-10-07 18:40Z).

    python conform/stamp.py "<headline>"                    print the title and first line
    python conform/stamp.py --check "<title>" <createdTime>  refuse a time not the doc's

The doc is created by a tool call, not a shell, so no one command can both read the clock and
create the doc. The first mode prints the title from the clock for the very next call to copy
verbatim; the second reads the post back against Drive's own createdTime -- the clock that made
the doc -- so a typed time that diverges is caught, not trusted. Five untimed stamps on
2026-10-07 were each corrected by hand; this is the check that fires instead.
"""

from __future__ import annotations

import re
import sys
from datetime import datetime, timedelta, timezone

sys.dont_write_bytecode = True

LATE = timedelta(minutes=2)          # a title is read, then the doc is made: never earlier


def now() -> datetime:
    return datetime.now().astimezone()


def zone(t: datetime) -> str:
    h = t.utcoffset() // timedelta(hours=1)
    return {-5: "CDT", -6: "CST"}.get(h, f"UTC{h:+d}")


def title(headline: str, t: datetime) -> str:
    return f"Seat -> Reviewer -- {t:%Y-%m-%d %H:%M} {zone(t)} (stamped {t:%H:%M:%S}) -- {headline}"


def check(text: str, created: str) -> str | None:
    """None when the doc was created in the titled minute or the next, else why not."""
    m = re.search(r"(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}) (C[DS]T)", text)
    if m is None:
        return "no CDT/CST stamp in the title"
    tz = timezone(timedelta(hours=-5 if m.group(3) == "CDT" else -6))
    stamped = datetime.strptime(f"{m.group(1)} {m.group(2)}", "%Y-%m-%d %H:%M")
    stamped = stamped.replace(tzinfo=tz)
    made = datetime.fromisoformat(created.replace("Z", "+00:00")).astimezone(tz)
    if not (stamped <= made < stamped + LATE):
        return f"titled {stamped:%H:%M}, created {made:%H:%M:%S} {m.group(3)}"
    return None


if __name__ == "__main__":
    if sys.argv[1:2] == ["--check"]:
        why = check(sys.argv[2], sys.argv[3])
        print(why or "stamp matches createdTime")
        sys.exit(1 if why else 0)
    t = now()
    print(title(" ".join(sys.argv[1:]), t))
    print(f"Seat -> Reviewer -- {t:%Y-%m-%d %H:%M:%S} {zone(t)} (from the clock, not typed)")
