"""R2, THE KEYED-PROBE READ, the ledger half (the reviewer 2026-10-21 16:48). Over one game's ledger:
(a) LOOKUP: every ROUTE lookup_tiers row -- entries listed per tier (T1a-c are keyed by the
    residual's delta kind and its rungs; T2, T3, T1d, T4, T5 are not), the entries a T1 offer
    deferred, and the late (T1d/T4/T5) entries the step's budget left unasked. Walked outside T1
    = listed outside T1 - deferred - late not asked: the entries a T1-only key would not walk.
    Per step and whole game. Units are ENTRIES, not compile calls.
(b) INVENTION: every MINT row's cut_counts -- not-novel (the candidate's name is already an atom
    or a library key) and recipe-held (its chain is a held recipe), against candidates_tried.
argv: ledger.jsonl [...]"""
import collections
import json
import sys

T1 = ("T1a", "T1b", "T1c")


def read(path):
    per = collections.defaultdict(collections.Counter)
    mint = collections.Counter()
    with open(path, encoding="utf-8") as fh:
        for ln in fh:
            if '"lookup_tiers"' not in ln and '"cut_counts"' not in ln:
                continue
            r = json.loads(ln)
            d = r.get("detail") or {}
            if r.get("event") == "lookup_tiers":
                c = per[r.get("cycle")]
                lst = d.get("listed") or {}
                t1 = sum(lst.get(t, 0) for t in T1)
                rest = sum(v for k, v in lst.items() if k not in T1)
                c["lookups"] += 1
                c["with_dk"] += d.get("dk") is not None
                c["listed_T1"] += t1
                c["listed_rest"] += rest
                c["deferred"] += d.get("deferred", 0)
                c["deferring_lookups"] += bool(d.get("deferred"))
                c["late_not_asked"] += d.get("late_not_asked", 0)
                c["walked_rest"] += max(0, rest - d.get("deferred", 0) - d.get("late_not_asked", 0))
                for k, v in lst.items():
                    c["tier:" + k] += v
            elif "cut_counts" in d:
                mint["mint_rows:" + r.get("event", "?")] += 1
                mint["candidates_tried"] += d.get("candidates_tried", 0)
                for k, v in (d.get("cut_counts") or {}).items():
                    mint["cut:" + k] += v
    return per, mint


for path in sys.argv[1:]:
    per, mint = read(path)
    print(f"== {path}")
    tot = collections.Counter()
    for cyc in sorted(per):
        tot.update(per[cyc])
        c = per[cyc]
        print(f"c{cyc}: lookups {c['lookups']} (dk {c['with_dk']}) | listed T1 {c['listed_T1']} "
              f"rest {c['listed_rest']} | deferred {c['deferred']} in {c['deferring_lookups']} | "
              f"late not asked {c['late_not_asked']} | walked outside T1 {c['walked_rest']}")
    print("whole game:", dict(sorted(tot.items())))
    print("mint:", dict(sorted(mint.items())))
