import sys

sys.dont_write_bytecode = True
p = sys.argv[1]
s = open(p, encoding="utf-8").read()
anchor = "- **4d-x, A WIN ENDS THE STREAM'S SLICE"
i = s.index(anchor)
j = s.index("\n", i) + 1
LINE = (
    "- **C1 (A), THE OVERRUN SAFETY NET, SINGLE AGENT (TETHER_CAP_INNER, TETHER_END_RESERVE, default ON; "
    "Isaiah 2026-10-22 12:36-12:37; the reviewer 12:37, 15:17, 15:24, 15:34, 15:40; C1 item 1, scope A, "
    "folded in).** cap.py: AT (the thinking deadline: the runner's deadline less the end-path reserve), "
    "head(), hold() (re-entrant, restored on any exit), held (entry head + hold), holding (hold, no entry "
    "head), CapReached (a BaseException, so interface._is_relational's \"except Exception\" cannot swallow a "
    "cut and no fault catch reads one). cap.head() at the top of 278 growing loops on the step path "
    "(the census: 257 loops in tether.py, 106 in 12 other modules, each READ and classed; 47 + 31 fixed "
    "loops get none). Agent.step wraps the old body: cap.AT set for the step and cleared after (so the "
    "end path is never cut); one catch writes \"@cap\" \"cap_mid_step\" (at = the scope the cut left, site "
    "= file:line, acted, \"unreached at this budget\", never a verdict); ag._cut set (also by _cap_end), "
    "and step's first line returns at once after it (\"after_cut\"), so after a cut only the END PATH "
    "reads what it left (the reviewer 15:34 (a)). HELD, because the end path (end_run, the lineage "
    "write, save_only, Gamma.save: their reads taken by AST) reads them: perceive (cap.holding: no entry "
    "head, so no cut lands between step's _ruin_step key and the press, the reviewer 15:40), "
    "diagnose._diagnose and Agent._land_kind (cap.held), _mint from gamma.accept through "
    "chain.note_mint and sweep's pays branch (with cap.hold()). NOT HELD, by ruling (15:40): _mint's and "
    "sweep's gamma.book counters, _leave_check's _line_grade counters (exclusive branches), step's "
    "_ruin_step (reset then set) and step's cycle (advanced once on every path), each whole at any cut. "
    "NEXT-STEP-ONLY marks, unreachable after a cut by (a), left as they are: _d5_split's and "
    "_recurse_parts' bound pop/restore, _derived_wants' _dw_tried, _invent's _inv_seen, _library_reach's "
    "_lib_offers resets, _muse_last, _shown_key, _integral. CHECK 1: no bare \"except:\" or \"except "
    "BaseException\" on the step path (tether.py; the 120 functions of the cross-module walk, which does "
    "not follow calls through untyped variables), and no \"except Exception\" there does cleanup a "
    "BaseException cut would skip. REMAINING UNCUT WORK: the held units above; whole single calls into "
    "other modules between two heads; _hold_invention's accept span (the same shape as _mint's, not in "
    "the ruled list). Item 1: _hyp_propose's cut writes the goal_hypotheses row with pick None, capped "
    "{at, checked, unreached} and never _hyp_exhausted. THE RESERVE: play times its end path from "
    "end_run (\"@run\" \"end_path\" row); lineage.write stores the wall and the sleep part in the store's "
    "meta after the game's sleep; the next life's load sets ag._end_reserve; a boundary write never lowers "
    "it; play breaks on ag._cut; unmeasured on a cold lineage (no reserve taken). e4_stream sets no "
    "deadline and none is added (15:24). tests/test_cap_inner.py: SW, DA (+ MF hold off), RG (+ MF), RS "
    "(+ MF off), H1, PH per family P1-P15 with AC (+ MF off), ID (no deadline, ON vs OFF: 1,665 rows "
    "equal), ES. The census and its readings: the design post 2026-10-22 15:14 and the data doc "
    "\"C1 (A) STATIC CENSUS\"; the WIP backup branch backup/wip/c1-heads.\n")
assert "C1 (A), THE OVERRUN SAFETY NET, SINGLE AGENT" not in s
s = s[:j] + LINE + s[j:]
open(p, "w", encoding="utf-8", newline="\n").write(s)
print("inserted after", s[:j].count("\n"))
