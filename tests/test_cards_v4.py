"""CARDS v4 + THE TIER CONTRAST (library/tether_rules.json v4; TETHER_TIER_CONTRAST default ON; the
reviewer r1948/r1949/r1952; design docs/04-PLANS_AHEAD/02-BUILD_SEQUENCE_FUTURE_STATE.md item 3).
  C1  build_library.py --check holds the v4 bytes (rc 0)
  C2  the four corrections are in the cards: (a) worked examples on the state/structure pair,
      (b) Three texts' on_refuted (CONTEXT -> a subgoal), (c)+(g) reach counts contact and
      budget, (e) the new card "Could it have come out the other way"; every figure quote in the
      changed and new cards is verbatim in docs/01-FOUNDATIONS/03-FIGURES_TEXT.md
  C3  _tier_contrast: J changed on every step -> 0.0; on no step -> 0.0; K opened only when J
      changed -> positive; K opened as often without J -> not positive
  C4  _tier_candidates on a gridworld agent with a planted tier-2 rule: ON offers the J with a
      positive contrast and drops the J that changed on every step. MF-C4 OFF: the every-step J
      is offered (counted by n alone)
Seconds (C1 runs the library check).
    python tests/test_cards_v4.py
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys

os.environ["TETHER_AGENT_SEED"] = "0"

import _repo  # noqa: F401,E402  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import gamma  # noqa: E402
import gridworld  # noqa: E402
import ledger  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402

ROOT = _repo.ROOT


def figure_text() -> str:
    """The figure text with the line numbers stripped and the lines joined, so a quote that runs
    across two numbered lines is found."""
    with open(os.path.join(ROOT, "docs", "01-FOUNDATIONS", "03-FIGURES_TEXT.md"),
              encoding="utf-8") as fh:
        lines = [re.sub(r"^\s*\d+\s{2}", "", ln.rstrip("\n")) for ln in fh]
    return " ".join(lines)


def main() -> None:
    r = subprocess.run([sys.executable, "-B", "library/build_library.py", "--check"], cwd=ROOT,
                       capture_output=True, text=True)
    assert r.returncode == 0 and "tether_rules.json: OK" in r.stdout, ("C1", r.stdout[-800:])
    print("  C1: build_library --check holds the v4 bytes")

    with open(os.path.join(ROOT, "library", "tether_rules.json"), encoding="utf-8") as fh:
        cards = json.load(fh)
    e = cards["entries"]
    assert cards["meta"]["version"].startswith("v4")
    assert e["TETHER|A state asks for its structure"]["examples"]
    assert e["TETHER|A structure asks for its states"]["examples"]
    assert "SUBGOAL" in e["TETHER|Three texts before acting"]["on_refuted"]["context"]
    asks = " ".join(e["TETHER|Could it be reached at all"]["asks"])
    assert "contact" in asks and "budget" in asks, asks
    new = e["TETHER|Could it have come out the other way"]
    assert new["when"] and new["asks"] and new["do"] and new["refuted_by"]
    figs = figure_text()
    quotes = []
    for key in ("TETHER|Could it be reached at all", "TETHER|Could it have come out the other way"):
        for b in e[key]["because"]:
            m = re.search(r'"(.+)"\s*$', b)
            if m and (b.startswith("Fig") or b.startswith("Symbols table")):
                quotes.append(m.group(1))
    for q in quotes:
        parts = [p for p in re.split(r"\s*/\s*", q) if p]     # the Symbols table rows, joined
        assert all(p in figs for p in parts), ("C2: a quote is not verbatim", q)
    print(f"  C2: (a) (b) (c)+(g) (e) in the cards; {len(quotes)} figure quotes verbatim")

    c = tether.Agent._tier_contrast
    assert c({"opened": 3, "after": {"j": 3}, "steps": 10, "j_steps": {"j": 10}}, "j") == 0.0
    assert c({"opened": 3, "after": {"j": 0}, "steps": 10, "j_steps": {}}, "j") == 0.0
    pos = c({"opened": 3, "after": {"j": 3}, "steps": 10, "j_steps": {"j": 4}}, "j")
    assert pos > 0, pos
    flat = c({"opened": 4, "after": {"j": 2}, "steps": 10, "j_steps": {"j": 5}}, "j")
    assert flat <= 0, flat
    print(f"  C3: contrast 0.0 for every step and no step, {pos:.2f} when K opens only with J, "
          f"{flat:.2f} when K opens as often without it")

    def offered(on: bool) -> list:
        tether._TIER_CONTRAST = on
        env = world.bind(gridworld.family("default", 0))
        ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="fam_default_0"), tether.Config(),
                          ledger.Ledger())
        ag.step()
        kinds = {"goal.x": "K", "a.x": "J1", "b.x": "J2"}
        ag._can_kind_key = lambda s: kinds.get(s, "other")
        ag._objs_named = lambda s: {s.partition(".")[0]}
        ag._res = {"goal.x": [1.0], "a.x": [1.0], "b.x": [1.0]}
        ag._tier2 = {"K": {"opened": 3, "after": {"J1": 3, "J2": 3}, "steps": 10,
                           "j_steps": {"J1": 10, "J2": 4}}}
        return [s for s, _why in ag._tier_candidates("goal.x")]

    on, off = offered(True), offered(False)
    assert on == ["b.x"], ("C4: ON should offer only the contrasting J2", on)
    assert "a.x" in off, ("MF-C4: OFF should offer the every-step J1", off)
    tether._TIER_CONTRAST = True
    print(f"  C4 ON: {on} (J1 changed on every step, dropped); MF-C4 OFF: {off} -> RED as required")
    print("cards_v4: OK")


if __name__ == "__main__":
    main()
