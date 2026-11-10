"""7c, THE NSM TRACE MADE READABLE (TETHER_NSM_DEDUPE; grammar.json's nsm words; the reviewer
2026-11-04 r1050, r1052, r1063, r1070, r1073). The 12-step gridworld ledger (LOOKUP 86% of its trace
before 7c) replayed through nsm.Speaker; the translator's word map. About a minute.

MF-D1  (r1073, "describe only what varied") the LOOKUP share falls; every BET / PARK / WANT row
       is SAID or COUNTED -- its (kind, cycle) count line holds exactly the rows and slots the
       ledger says -- and a slot whose text changed since its last said line is always SAID;
       said > 0 and same > 0. With TETHER_NSM_DEDUPE=0 there are no count lines (the arm-OFF red)
MF-D2  row-truth: every line cites real rows that say its kind; 0 unlisted capitals
MF-D3  every one of the eight bonds has a word, the word -> bond map is injective, and a sentence
       with each bond's word reads back to that bond (Isaiah 2026-11-04 08:51, r1072: − THERE IS
       NOT, ∥ MAYBE; RED on the grammar.json before it, where ¬ and − both read NOT and ∥ had none)

    python tests/test_nsm_7c.py
"""
from __future__ import annotations

import collections
import json
import os
import re
import sys
import tempfile
from pathlib import Path

os.environ["TETHER_AGENT_SEED"] = "0"

import _repo  # noqa: F401,E402  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import gamma  # noqa: E402
import gridworld  # noqa: E402
import ledger  # noqa: E402
import nsm  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402

LINE = re.compile(r"^c(\d+) #(\d+)(?:\.\.#(\d+))? ([A-Z_]+) (\S+):")
ENDS = (ledger.WIN, ledger.ADVANCE)


def ledger_rows(td: Path) -> list:
    env = world.bind(gridworld.family("default", 0))
    led = ledger.Ledger(path=str(td / "run.jsonl"))
    ag = tether.Agent(env, gamma.Gamma(env.atoms(), game="fam_default_0"), tether.Config(), led)
    for _ in range(12):
        ag.step()
    ag.end_run("cap")
    return [json.loads(x) for x in (td / "run.jsonl").read_text(encoding="utf-8").splitlines()
            if x.strip()]


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    with tempfile.TemporaryDirectory() as td:
        rows = ledger_rows(Path(td))
        log = (Path(td) / "nsm.log").read_text(encoding="utf-8").splitlines()
    by_seq = {r["seq"]: r for r in rows}
    rows_of = collections.Counter()               # (kind, cycle) -> rows the ledger says
    slots_of = collections.defaultdict(set)       # (kind, cycle) -> their slots
    changed, last = set(), {}                     # (kind, slot, cycle) whose text changed
    for r in sorted(rows, key=lambda r: r["seq"]):
        for k, txt in nsm.say_row(r["event"], r.get("detail", {}), ENDS):
            if k in ("BET", "PARK", "WANT"):
                rows_of[(k, r["cycle"])] += 1
                slots_of[(k, r["cycle"])].add(r.get("slot"))
                if last.get((k, r.get("slot"))) != txt:
                    changed.add((k, r.get("slot"), r["cycle"]))
                last[(k, r.get("slot"))] = txt
    count = {}
    have, kinds, wrong, unl = set(), collections.Counter(), [], 0
    for ln in log:
        m = LINE.match(ln)
        assert m, ("unparsed", ln[:100])
        kinds[m[4]] += 1
        if m[5] != "@":
            have.add((m[4], m[5], int(m[1])))
        else:
            c = re.search(r"(\d+) slots, (\d+) said, (\d+) the same as before", ln)
            if c:
                count[(m[4], int(m[1]))] = tuple(int(x) for x in c.groups())
        for s in {int(m[2]), int(m[3] or m[2])}:
            r = by_seq.get(s)
            ks = [] if r is None else [k for k, _t in nsm.say_row(r["event"], r.get("detail", {}),
                                                                  ENDS)]
            if m[4] not in ks:
                wrong.append((s, m[4], ln[:90]))
        unl += bool(nsm.unlisted(ln.split(": ", 1)[1]))
    total = sum(kinds.values())
    share = kinds["LOOKUP"] / max(total, 1)
    per = collections.Counter(k for k, _c in rows_of)
    assert all(per[k] > 0 for k in ("BET", "PARK", "WANT")), ("MF-D1 has no occasion", per)
    bad = [(kc, rows_of[kc], len(slots_of[kc]), count.get(kc)) for kc in rows_of
           if count.get(kc) is None or count[kc][1] + count[kc][2] != rows_of[kc]
           or count[kc][0] != len(slots_of[kc])]
    assert not bad, ("MF-D1: rows neither said nor counted", len(bad), bad[:4])
    unsaid = sorted(changed - have)
    assert not unsaid, ("MF-D1: a changed text was not said", len(unsaid), unsaid[:4])
    said_n = sum(v[1] for kc, v in count.items() if kc[0] in per)
    same_n = sum(v[2] for kc, v in count.items() if kc[0] in per)
    assert said_n > 0 and same_n > 0, ("MF-D1: said and same both > 0", said_n, same_n)
    assert share < 0.86, ("MF-D1: the LOOKUP share did not fall", round(share, 3), dict(kinds))
    assert log and not wrong and not unl, ("MF-D2", wrong[:3], unl)
    w = nsm.words()
    said = [v for v in w.values() if v]
    assert len(said) == len(w) == 8, ("MF-D3: a bond has no word", w)
    assert len(said) == len(set(said)), ("MF-D3: a word names two bonds", w)
    inc = next(a for a in gamma.Gamma(world.bind(gridworld.family("default", 0)).atoms(),
                                      game="fam_default_0").atoms if a.in_type == a.out_type)
    st = nsm.say_term(gamma.Term((inc,)))
    atoms = {inc.name: inc}
    back = {}
    for bond, word in w.items():
        if not word:
            continue
        got = nsm.read_node(f"([{st}] {word} [{st}])", atoms)
        reason = getattr(got, "reason", "")
        back[bond] = "→ read back" if bond == "→" else reason.split(" ")[0]
        assert (bond == "→" and not reason) or reason.startswith(bond), ("MF-D3 read back", bond,
                                                                       word, reason)
    print(f"  MF-D1 LOOKUP share {share:.1%} (86% before 7c) over {total} lines {dict(kinds)}; "
          f"BET/PARK/WANT rows {sum(rows_of.values())}: said {said_n}, the same as before "
          f"{same_n}, every row said or counted, all {len(changed)} changed texts said")
    print("  MF-D2 every line cites rows that say it; unlisted capitals 0")
    print(f"  MF-D3 words {w}; each word reads back to its own bond: {back}")
    print("test_nsm_7c OK")


if __name__ == "__main__":
    main()
