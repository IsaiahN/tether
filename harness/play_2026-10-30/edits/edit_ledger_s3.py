p = "C:/TETHER_RUNS/S6_2026-10-19/wt_ivv/docs/LEDGER.md"
s = open(p, encoding="utf-8", newline="").read()
assert "\r\n" not in s
lines = s.split("\n")
i = next(n for n, x in enumerate(lines) if x.startswith("- **W1 / W2, THE STORE'S KEY MEMOS"))
new = ("- **THE CONTACT-MINT READ (S3A, S3B, S3C; the reviewer 2026-10-21 16:48, 17:01, 17:18, 17:28): vc33's two pair-contact "
       "want-only mints are ONE path, the objective's unseen-value walk.** S3B (c1d0f0a): py-spy (C:/TETHER_RUNS/tools/spyenv, "
       "--subprocesses: the venv exe is a launcher stub) and cProfile AGREE: ~98% of o0~o2.contact (c3, 24.9 s) and o11~o2.contact "
       "(c6, 143.2 s) is _cannot_pay -> _value_of -> objective_step -> _priced_hit -> _sat -> gamma.apply (16.2M apply calls at c3, "
       "87.3M at c6). S3C: at c3 the 7,477 _priced_hit walks are all ORDERED over an 8,193-value alphabet; 1,934 found NOTHING and made "
       "15,843,328 of the 16,140,721 evaluations (98.2%), 0 true -- the cost is the proof of absence over the whole alphabet (the cd82 "
       "shape of the 10-08 ruling, back through A1 site 9's unseen pricing, TETHER_A1_DOMAIN). All 19 atoms in the 35 shapes seen are "
       "piecewise-constant in the slot value with breakpoints at ctx values (the operand, the group, 0) or constant in it, and only "
       "a chain's first atom sees the value: the interval bound (Fig 12 :86-89, Fig 13 :20) would answer 7,477 of 7,477 walks; design "
       "posted 17:36, not built. OWNED: S3A's cap (--max-s 600, an unprofiled run's) was below the profiled run, and its rows were "
       "written at exit, so the supervisor took it at 600.8 s in c7 with nothing kept; S3B's cProfile run (cap 3000 s) was sized "
       "without Isaiah's 10-20 15:42 10-minute cap on new boxes, had started when the reviewer's 17:18 ruled it out, and ran to its end "
       "under never-kill (713.8 s, ~2 min over the cap's estimate). Rows are now written per call at once.")
lines.insert(i + 1, new)
j = next(n for n, x in enumerate(lines) if x.startswith("- **KAGGLE EXPORT LIST, step 14"))
k8 = (" (K8, the reviewer 2026-10-21 16:48) the export runs with the AGENT SEED SET (TETHER_AGENT_SEED), beside K6's "
      "PYTHONHASHSEED: Term.handle draws its suffix from Python's random when the agent seed is off, so the same game wrote different "
      "handles per process (found by test_store_key_memo's OFF-OFF control, which seeds random per game).")
assert "(K8," not in lines[j]
lines[j] = lines[j] + k8
open(p, "w", encoding="utf-8", newline="").write("\n".join(lines))
print("ok", i + 2, j + 1)
