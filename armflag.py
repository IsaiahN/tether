"""armflag: the ONE parser every capability arm is read through (Isaiah's ruling, 2026-10-08).

    "1" / "true"         ON
    "0" / "false" / ""   OFF
    anything else        refused -- a typo is not a setting

Eighteen arms were read as the truthiness of the raw environment string, so setting one to
"0" turned it ON: the string "0" is truthy. A run record stating an arm "=0" could
therefore describe an agent running with it on. Every arm now reads through `arm()`, and
`conform/arms.py` sets each one to "0" in a fresh process and asserts it reads OFF.
"""
from __future__ import annotations

import os

ON = ("1", "true")
OFF = ("0", "false", "")


def arm(name: str, default: bool = False) -> bool:
    """The arm's state: the environment's word if it says one, else the declared default."""
    raw = os.environ.get(name)
    if raw is None:
        return default
    v = raw.strip().lower()
    if v in ON:
        return True
    if v in OFF:
        return False
    raise ValueError(f"{name}={raw!r}: an arm reads 1/true (on) or 0/false/empty (off), "
                     f"nothing else")
