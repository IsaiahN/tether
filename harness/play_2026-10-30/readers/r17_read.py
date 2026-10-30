"""Read-only (the reviewer r286): PLAY17's new round-line columns, from one finished round's switch.tsv and
stream.jsonl. arrivals (arrival_gap rows), decided_by counts, bar values and shares, breaks applied,
appearance_disagrees, misses (switches with no frame_break at their first cycle), false breaks (frame_break rows
at a cycle that is not a switch's first). argv: play dir, round numbers."""
import collections
import json
import re
import sys

sys.dont_write_bytecode = True
P = sys.argv[1]
EV = re.compile(r'"event": "(arrival_gap|appearance_disagrees|frame_break)"')


def play18(rd: str) -> str:
    """r305's PLAY18 readings: instance_retired sums per round (dangling must be 0), and the live
    reuse set at the round's last REPEAT row (the last game)."""
    keys = ("retired", "kinds_new", "kinds_held", "repointed", "dropped")
    tot, rows, dang, last = dict.fromkeys(keys, 0), 0, 0, None
    for ln in open(f"{rd}/stream.jsonl", encoding="utf-8"):
        if '"event": "instance_retired"' in ln:
            d = json.loads(ln)["detail"]
            rows += 1
            for k in keys:
                tot[k] += d.get(k) or 0
            dang += len(d.get("dangling") or [])
        elif '"event": "repeat"' in ln:
            d = json.loads(ln)["detail"]
            if "gamma_reuse_live" in d:
                last = (d["gamma_reuse_live"], d.get("gamma_reuse_on_board"))
    return (f"instance_retired rows {rows}: " + ", ".join(f"{k} {v}" for k, v in tot.items())
            + f", dangling {dang} | live reuse at the last step {last[0] if last else None} "
            f"(on board {last[1] if last else None})")
SLOT = re.compile(r"\bo\d+(?:~o\d+)?\.[A-Za-z_0-9]+")
MINT_EV = ("mint", "accept", "pull", "reuse_install")


def harvest(rd: str, sw: dict) -> str:
    """Items 6 and 11 as ruled in r288. 6, approximate (bet-row join): each settle's (slot, held_out_cycle) joined
    to that cycle's PERCEIVE bet row: risky-held (predicted != from_value, actual == predicted), null-agreeing
    (predicted == from_value), contradicted (predicted != from_value, actual != predicted), no bet. 11, per
    game on slot: named by a PLAN goal_hypotheses pick and by a MINT mint/accept/pull/reuse_install row."""
    c0s = sorted(sw)

    def game(c):
        k = None
        for x in c0s:
            if c >= x:
                k = x
        return k
    bets, sets = {}, []
    plan, mint, route = {}, {}, {}     # (game, slot) -> first cycle; pull / reuse_install are ROUTE rows
    for ln in open(f"{rd}/stream.jsonl", encoding="utf-8"):
        if '"event": "bet"' in ln and '"step": "PERCEIVE"' in ln:
            r = json.loads(ln)
            bets[(r["cycle"], r["slot"])] = r["detail"]
        elif '"event": "settle"' in ln:
            r = json.loads(ln)
            sets.append((r["slot"], r["detail"]))
        elif '"event": "goal_hypotheses"' in ln:
            r = json.loads(ln)
            for s in SLOT.findall(str((r.get("detail") or {}).get("pick") or "")):
                plan.setdefault((game(r["cycle"]), s), r["cycle"])
        elif any(f'"event": "{e}"' in ln for e in MINT_EV):
            r = json.loads(ln)
            if SLOT.fullmatch(r["slot"]) and r["step"] in ("MINT", "ROUTE"):
                (mint if r["step"] == "MINT" else route).setdefault((game(r["cycle"]), r["slot"]),
                                                                     r["cycle"])
    k6 = collections.Counter()
    if sets and all("risky" in d for _s, d in sets):
        # TETHER_SETTLE_PRED: the settle row's own fields, exact (r288, r294); no join needed
        ex = collections.Counter("risky-held" if d["risky"] else "null-agreeing" for _s, d in sets)
        bad = sum(1 for _s, d in sets if d.get("actual_code") != d.get("predicted_code"))
        return_6 = (f"item 6 EXACT (settle row): settles {len(sets)}, risky-held {ex['risky-held']}, "
                    f"null-agreeing {ex['null-agreeing']}, code mismatches {bad}")
    else:
        return_6 = None
    for s, d in sets:
        b = bets.get((d.get("held_out_cycle"), s))
        if b is None or "actual" not in b:
            k6["no bet"] += 1
        elif b.get("predicted") == b.get("from_value"):
            k6["null-agreeing"] += 1
        else:
            k6["risky-held" if b["actual"] == b.get("predicted") else "contradicted"] += 1
    # r290: ONE join; bottom-up = every install that explains a slot's residual (MINT accept u ROUTE pull /
    # reuse_install), the step a sub-column
    up = {k: min(v for v in (mint.get(k), route.get(k)) if v is not None) for k in set(mint) | set(route)}
    both = set(plan) & set(up)
    u_first = sum(1 for k in both if up[k] < plan[k])
    p_first = sum(1 for k in both if plan[k] < up[k])
    six = return_6 or (f"item 6 approximate (bet-row join): settles {len(sets)}, risky-held "
                       f"{k6['risky-held']}, null-agreeing {k6['null-agreeing']}, contradicted "
                       f"{k6['contradicted']}, no bet {k6['no bet']}")
    return (f"{six} | "
            f"item 11 per game on slot: converged {len(both)} / PLAN-named {len(plan)} / BOTTOM-UP-named "
            f"{len(up)} (by step MINT {len(mint)}, ROUTE {len(route)}); order bottom-up first {u_first}, "
            f"PLAN first {p_first}, same cycle {len(both) - u_first - p_first}")


for n in sys.argv[2:]:
    rd = f"{P}/round_{int(n):02d}"
    sw = {}
    for ln in open(f"{rd}/switch.tsv", encoding="utf-8"):
        f = ln.rstrip("\n").split("\t")
        if f[0].isdigit():
            sw[int(f[3])] = (int(f[0]), f[1])
    first = min(sw) if sw else None
    gaps, dis, fb = [], 0, collections.Counter()
    for ln in open(f"{rd}/stream.jsonl", encoding="utf-8"):
        m = EV.search(ln)
        if not m:
            continue
        r = json.loads(ln)
        if m.group(1) == "arrival_gap":
            gaps.append((r["cycle"], r["detail"]))
        elif m.group(1) == "appearance_disagrees":
            dis += 1
        else:
            fb[r["cycle"]] += 1
    switches = {c: g for c, g in sw.items() if c != first}
    missed = [f"{g[1]}@{g[0]}" for c, g in sorted(switches.items()) if c not in fb]
    false = sorted(c for c in fb if c not in switches)
    by = collections.Counter(re.sub(r"n=\d+", "n=K", d.get("decided_by", "?")) for _c, d in gaps)
    bars = sorted({d.get("bar") for _c, d in gaps}, key=lambda x: (x is None, x))
    shares = sorted(d.get("share") for _c, d in gaps)
    applied = sum(1 for _c, d in gaps if d.get("applied"))
    decided = sum(1 for _c, d in gaps if d.get("broke"))
    off_switch = [c for c, _d in gaps if c not in switches]
    print(f"round {n}: switches {len(switches)} | arrivals {len(gaps)} (at a non-switch cycle: {off_switch or 0}) | "
          f"decided_by {dict(by)} | bar values {bars} | share min {shares[0] if shares else None} "
          f"max {shares[-1] if shares else None} | decided break {decided}, applied {applied} | "
          f"appearance_disagrees {dis} | frame_break rows {sum(fb.values())} | misses {len(missed)} {missed} | "
          f"false breaks {len(false)} {false}")
    print(f"  {harvest(rd, sw)}")
    print(f"  {play18(rd)}")
