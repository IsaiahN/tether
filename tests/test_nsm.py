"""BUILD 2 7 / 7b, THE NSM TRACE AND ITS TRANSLATION (TETHER_NSM_SPEAK; the reviewer r894 2,
r895 1-2, r953 4). The demo world (world.Transitions, which mints) and the library's compiled
terms; no game. About a minute.

MF-S1  a run with a ledger path writes nsm.log; every line cites seqs that are rows of the ledger,
       and the cited row says that line's kind (say_row on it gives the kind); RED on 2b5e08c (no
       nsm.log)
MF-S2  the ledger ON vs OFF differs only in the arms row (identity_mod_rows); OFF writes no nsm.log
MF-S3  a LOOKUP row holding 80 bonds (its sample 80) is said as 50 sentences plus "+30 MORE
       (`held_n 80, the row keeps 50`)"
MF-S4  a bond_tests / molecule_apply row over 0 frames is said "no window", never as a count
MF-S5  the park split is two sentences: "not found within budget" asks for MORE TIME, "closure
       cannot cover R" says NOT ONE THING I CAN SAY IS LIKE THIS
MF-S6  (r1001) every capitalised word of every template, and of every nsm.log line the run wrote,
       is an NSM prime or operator word grammar.json lists, or an inflection of one (ALLOLEX);
       the agent's names are fillers in backticks
MF-T   the round trip: every distinct term compiled from the library's candidates over gridworld's
       atoms, and every term the demo agent holds, is said and read back to an equal Term (atoms,
       operand, operand_term, guard, guard_ref); a → junction of two such terms reads back as their
       one chain or a listed typing refusal; every other bond, and "?", is refused with a listed
       reason. Unlisted reasons: 0

    python tests/test_nsm.py
"""
from __future__ import annotations

import collections
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

import compile_term  # noqa: E402
import composer  # noqa: E402
import gamma  # noqa: E402
import gridworld  # noqa: E402
import ledger  # noqa: E402
import nsm  # noqa: E402
import tether  # noqa: E402
import world  # noqa: E402

HERE = Path(__file__).resolve()
LINE = re.compile(r"^c(\d+) #(\d+)(?:\.\.#(\d+))? ([A-Z_]+)")
ENDS = (ledger.WIN, ledger.ADVANCE)


def child(out: str, env_extra: dict) -> None:
    env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "PYTHONHASHSEED": "0",
           "TETHER_AGENT_SEED": "0", **env_extra}
    r = subprocess.run([sys.executable, "-B", str(HERE), "--run", out], env=env,
                       capture_output=True, text=True, timeout=900)
    assert r.returncode == 0, r.stderr[-2000:]


def run(out: str) -> None:
    os.makedirs(out, exist_ok=True)
    env = world.bind(world.Transitions())
    led = ledger.Ledger(path=os.path.join(out, "run.jsonl"))
    ag = tether.Agent(env, gamma.Gamma(env.atoms()), tether.Config(), led)
    ag.run(16)
    ag.end_run("cap")
    terms = [{"name": t.name, "say": nsm.say_term(t)} for t in ag.gamma.library.values()]
    Path(out, "terms.json").write_text(json.dumps(terms), encoding="utf-8")


def rows(p: Path) -> list:
    return [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]


def same(a, b) -> bool:
    def k(t):
        return (tuple(x.name for x in t.atoms), t.operand, t.guard, t.guard_ref,
                None if t.operand_term is None else tuple(x.name for x in t.operand_term.atoms))
    return k(a) == k(b)


def library_terms(atoms: dict) -> dict:
    lib = tether._library()
    out = {}
    conds = set()
    for key in lib.seed:
        for role in ("STATE", "TEST", "PROCESS", "CAUSE"):
            for cand in lib.view(key, role):
                conds.update(cand[s] for s in ("condition", "if", "then") if s in cand)
    for c in sorted(conds):
        got = compile_term.compile_candidate({"condition": c}, atoms)
        if isinstance(got, compile_term.Compiled):
            out.setdefault(got.term.name, got.term)
    return out


def round_trip(terms: dict, atoms: dict) -> dict:
    n = bad = 0
    unlisted, reasons = [], collections.Counter()
    for t in terms.values():
        n += 1
        back = nsm.read_term(nsm.say_term(t), atoms)
        if isinstance(back, compile_term.Refusal) or not same(t, back):
            bad += 1
            unlisted.append((t.name, nsm.say_term(t), getattr(back, "reason", back)))
    # a junction joins two plain chains: each term's own atoms (the library's terms carry an
    # operand or a guard, which a junction refuses)
    plain = list({t.name: t for t in (gamma.Term(x.atoms) for x in terms.values())}.values())[:25]
    j = 0
    for a in plain:
        for b in plain:
            for bond in composer.BONDS + (composer.UNKNOWN,):
                j += 1
                node = composer.bind(bond, a, b)
                back = nsm.read_node(nsm.say_node(node), atoms)
                if isinstance(back, compile_term.Refusal):
                    reasons[back.reason.split(" [")[0][:60]] += 1
                    if not nsm.listed(back.reason):
                        unlisted.append((nsm.say_node(node), back.reason))
                    if bond == "→" and "does not accept" not in back.reason:
                        unlisted.append(("→ refused for no typing reason", back.reason))
                elif bond != "→" or tuple(x.name for x in back.atoms) != tuple(
                        x.name for x in a.atoms + b.atoms):
                    unlisted.append(("→ read back wrong", nsm.say_node(node), back.name))
    return {"terms": n, "bad": bad, "junctions": j, "unlisted": unlisted,
            "refusals": dict(reasons.most_common(8))}


def main():
    if "--run" in sys.argv:
        run(sys.argv[sys.argv.index("--run") + 1])
        return
    sys.stdout.reconfigure(encoding="utf-8")      # the refusals name bonds (⇒, ∥)
    sys.path.insert(0, str(HERE.parent.parent / "conform"))
    import identity_mod_rows
    assert nsm.words().get("→") == "AFTER", ("the grammar's → word", nsm.words())

    lk = {"held_n": 80, "held_sample": [{"molecule": f"M{i}", "left": "A", "right": "B",
                                         "left_reading": "o1.row", "right_reading": "o1.col",
                                         "held": ["→"]} for i in range(80)]}
    s3 = nsm.say_row("lookup", lk, ENDS)
    assert len(s3) == 51 and s3[-1][1] == "+30 MORE (`held_n 80, the row keeps 50`)", (
        "MF-S3", s3[-1])
    for ev in ("bond_tests", "molecule_apply"):
        s4 = nsm.say_row(ev, {"frames": 0, "tested": 14, "offers": 3}, ENDS)
        assert len(s4) == 1 and s4[0][0] == "NO_WINDOW" and "no window" in s4[0][1] and \
            "14" not in s4[0][1] and "3" not in s4[0][1].replace(ev, ""), ("MF-S4", s4)
    a = nsm.say_row("park", {"verdict": "not found within budget"}, ENDS)
    b = nsm.say_row("park", {"verdict": "closure cannot cover R"}, ENDS)
    assert a != b and "MORE TIME" in a[0][1] and "NOT ONE THING I CAN SAY" in b[0][1], (
        "MF-S5", a, b)
    every = [s for ev, d in (("lookup", lk), ("bond_tests", {"frames": 0}),
                             ("park", {"verdict": "not found within budget"}),
                             ("park", {"verdict": "closure cannot cover R"}),
                             ("park", {"verdict": "depth_exhausted"}), ("mint", {"term": "inc"}),
                             ("molecule_offer", {"bond": "→", "seen": True, "molecule": "M"}),
                             ("molecule_offer", {"bond": "→", "seen": False, "molecule": "M"}),
                             ("bet", {"predicted": 1, "meant": "BECOME OTHER"}),
                             ("settle", {"term": "inc"}), ("demote", {"term": "inc"}),
                             ("settle", {"status": "refuted", "term": "inc"}),
                             ("want", {"objective": "ALL(x)"}), ("routine", {"routine": "r"}),
                             ("ending", {"how": ledger.WIN}), ("ending", {"how": ledger.ADVANCE}))
             for s in nsm.say_row(ev, d, ENDS)]
    bad6 = [(s, nsm.unlisted(t)) for s, t in every if nsm.unlisted(t)]
    assert len(every) == 68 and not bad6, ("MF-S6 templates", len(every), bad6)

    env = world.bind(gridworld.family("default", 0))
    gatoms = {x.name: x for x in gamma.Gamma(env.atoms(), game="fam_default_0").atoms}
    lt = library_terms(gatoms)
    rt = round_trip(lt, gatoms)
    assert rt["terms"] and rt["junctions"] and not rt["bad"] and not rt["unlisted"], (
        "MF-T library", rt["terms"], rt["junctions"], rt["bad"], rt["unlisted"][:5])

    with tempfile.TemporaryDirectory() as td:
        on, off = Path(td) / "on", Path(td) / "off"
        child(str(on), {})
        child(str(off), {"TETHER_NSM_SPEAK": "0"})
        led = rows(on / "run.jsonl")
        by_seq = {r["seq"]: r for r in led}
        log = (on / "nsm.log").read_text(encoding="utf-8").splitlines()
        wrong = []
        for ln in log:
            m = LINE.match(ln)
            if m is None:
                wrong.append(("unparsed", ln))
                continue
            for s in {int(m[2]), int(m[3] or m[2])}:
                r = by_seq.get(s)
                kinds = [] if r is None else [k for k, _t in nsm.say_row(
                    r["event"], r.get("detail", {}), ENDS)]
                if m[4] not in kinds:
                    wrong.append((s, m[4], kinds, ln[:120]))
        assert log and not wrong, ("MF-S1", len(log), wrong[:3])
        not_prime = [(ln[:100], nsm.unlisted(ln.split(": ", 1)[1])) for ln in log
                     if nsm.unlisted(ln.split(": ", 1)[1])]
        assert not not_prime, ("MF-S6", not_prime[:3])
        diff = identity_mod_rows.compare(rows(off / "run.jsonl"), led, set())
        assert all(d.startswith("seq 0 (arms)") for d in diff), ("MF-S2", diff[:3])
        assert not (off / "nsm.log").exists(), "MF-S2 OFF wrote nsm.log"
        kinds = collections.Counter(LINE.match(x)[4] for x in log if LINE.match(x))
        dt = json.loads((on / "terms.json").read_text(encoding="utf-8"))
        datoms = {x.name: x for x in world.Transitions().atoms()}
        held_bad = []
        for t in dt:
            back = nsm.read_term(t["say"], datoms)
            if isinstance(back, compile_term.Refusal) or nsm.say_term(back) != t["say"]:
                held_bad.append((t["name"], t["say"], getattr(back, "reason", None)))
        assert dt and not held_bad, ("MF-T held", held_bad[:3])
        sample = log[:6]
    print(f"  MF-S1 {len(log)} lines, every one cites a ledger row that says it: {dict(kinds)}")
    for x in sample:
        print("     ", x[:150])
    print(f"  MF-S2 ledger ON vs OFF: {len(diff)} difference(s), the arms row only; OFF no file")
    print("  MF-S3 80 held: 50 sentences + '+30 more held; the row keeps 50'")
    print("  MF-S4 0 frames: 'no window' for bond_tests and molecule_apply")
    print(f"  MF-S5 park: {a[0][1]!r} / {b[0][1]!r}")
    print(f"  MF-T library: {rt['terms']} terms read back equal; {rt['junctions']} junctions, "
          f"refusals {rt['refusals']}; held by the demo agent: {len(dt)} equal; unlisted 0")
    print("test_nsm OK")


if __name__ == "__main__":
    main()
