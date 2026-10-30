import collections, json, sys
sys.dont_write_bytecode = True
f = sys.argv[1]
sv, ss, gap, plan_terms, mint_ev = collections.Counter(), collections.Counter(), collections.Counter(), collections.Counter(), collections.Counter()
ex = {}
for ln in open(f, encoding="utf-8"):
    if '"step": "MINT"' not in ln and '"step": "PLAN"' not in ln and '"event": "settle"' not in ln:
        continue
    r = json.loads(ln); d = r.get("detail") or {}; e = r["event"]
    if e == "settle":
        sv[d.get("verdict")] += 1; ss[(d.get("status"), d.get("ground_said"))] += 1
        fo, ho = d.get("fitted_through"), d.get("held_out_cycle")
        gap[(ho - fo) if isinstance(fo, int) and isinstance(ho, int) else None] += 1
    elif r["step"] == "PLAN" and "pick" in d:
        plan_terms[type(d["pick"]).__name__] += 1
        if d["pick"] and "plan_pick" not in ex: ex["plan_pick"] = d["pick"]
    elif r["step"] == "MINT" and "term" in d:
        mint_ev[e] += 1
        ex.setdefault("mint_" + e, d["term"])
print("settle verdicts", dict(sv)); print("settle (status, ground_said)", dict(ss)); print("held_out - fitted_through", dict(gap))
print("PLAN pick types", dict(plan_terms)); print("MINT events with term", dict(mint_ev)); print("examples", json.dumps(ex, default=str)[:900])
