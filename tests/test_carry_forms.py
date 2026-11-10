"""BUILD 3 ITEM 11: A CARRIED RULE IN ITS TURNED AND MIRRORED FORMS (TETHER_CARRY_FORMS; the
reviewer 2026-11-04 r1152). library_runtime.axis_forms was written for this ("a carried rule is
offered in all of them at the destination; the ground there decides which holds") and only
Library.carry, which no agent path calls, produced the forms. Now _reinvent_carried re-invents each
carried template's forms too, each its own entry on trial. Seconds: a gridworld agent, one carried
record, the method called.

MF-F1  a carried "{o}.row < {x}.row" is re-invented with its three forms -- turned "{o}.col <
       {x}.col", mirrored "{o}.row > {x}.row", turned+mirrored "{o}.col > {x}.col" -- named
       <name>~<form>, receipts naming the form and the rule it came from
MF-F2  a condition with no axis and no order (e.g. "{o}.colour == {x}.colour") has no other form:
       only the rule itself
The red is behavioural, the arm OFF on this tree: TETHER_CARRY_FORMS=0 fails MF-F1.

    python tests/test_carry_forms.py
"""
from __future__ import annotations

import os
import sys

os.environ["TETHER_AGENT_SEED"] = "0"

import _repo  # noqa: F401,E402  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import gamma  # noqa: E402
import gridworld  # noqa: E402
import ledger  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402


def carried(template, name):
    env = world.bind(gridworld.family("default", 0))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="fam_default_0"), tether.Config(),
                      ledger.Ledger())
    out = ag._reinvent_carried([{"name": name, "template": template, "game": "g1",
                                 "affects": []}])
    lib = ag._inv_library()
    return out, {k: lib.get(k) for k in list(lib.runtime) if name in k}


def main():
    t = "{o}.row < {x}.row"
    out, got = carried(t, "Below")
    want = {"Below~turned": "{o}.col < {x}.col", "Below~mirrored": "{o}.row > {x}.row",
            "Below~turned+mirrored": "{o}.col > {x}.col"}
    have = {k.split("|", 1)[1]: (e.get("run") or {}).get("condition_text") for k, e in got.items()}
    forms = {n: c for n, c in have.items() if n != "Below"}
    assert have.get("Below") == t and forms == want and out["reinvented"] == 4, (
        "MF-F1: the turned / mirrored forms are not re-invented", have, out)
    rec = (got["AGENT-INVENTED|Below~turned"].get("born") or {}).get("receipt") or {}
    assert rec.get("form") == "turned" and rec.get("form_of") == "Below", ("MF-F1 receipt", rec)
    print(f"  MF-F1 {t!r} -> {forms}")
    out2, got2 = carried("{o}.colour == {x}.colour", "Same")
    assert list(got2) == ["AGENT-INVENTED|Same"] and out2["reinvented"] == 1, ("MF-F2", got2)
    print("  MF-F2 an axis-free, order-free rule has no other form: only itself")
    print("test_carry_forms OK")


if __name__ == "__main__":
    main()
