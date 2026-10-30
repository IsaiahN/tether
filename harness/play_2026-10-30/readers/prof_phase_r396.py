import pstats, sys
sys.dont_write_bytecode = True
names = ("route", "_mint_in_step", "perceive", "indistinguishable", "_g1_wants", "_derived_wants",
         "_narrate_cues", "choose", "_hyp_propose", "_goal_hypothesis")
for g in ("ft09", "lp85", "sp80"):
    st = pstats.Stats(sys.argv[1] + f"/{g}.pstats").stats
    step = max(v[3] for f, v in st.items() if f[2] == "step" and f[0].endswith("tether.py"))
    row = []
    for n in names:
        hits = [(f, v) for f, v in st.items() if f[2] == n and f[0].endswith("tether.py")]
        ct = max((v[3] for _f, v in hits), default=0.0)
        row.append(f"{n} {ct / step:.1%}")
    print(g, f"step_ct {step:.1f}s |", " | ".join(row))
