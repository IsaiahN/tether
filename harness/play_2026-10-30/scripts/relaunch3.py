"""r355 (c): PLAY19's round-3 relaunch edits -- FIRST_ROUND=3, the want's box hash, and the precheck's gates
(head 330dd0a5, round_02 kept / no round_03, the CREDIT pin in the box, LOG_INDEX verify on round_02). argv: PLAY19 dir."""
import sys

sys.dont_write_bytecode = True
P = sys.argv[1].rstrip("/")


def edit(name, pairs):
    p = f"{P}/{name}"
    s = open(p, encoding="utf-8", newline="").read()
    nl = "\r\n" if "\r\n" in s else "\n"
    for a, b in pairs:
        a, b = a.replace("\n", nl), b.replace("\n", nl)
        assert s.count(a) == 1, (name, a[:70], s.count(a))
        s = s.replace(a, b)
    open(p, "w", encoding="utf-8", newline="").write(s)


edit("play_chain.sh", [
 ("FIRST_ROUND=2\n",
  "# RELAUNCH 3 (Isaiah 2026-10-29 15:50 \"you can switch off credit\"; the reviewer r355): round 2 ended by the\n"
  "# STOP file (CLEAN STOP before round 3, head 330dd0a5); the chain CONTINUES at round 3 with TETHER_DIVIDE_CREDIT=0\n"
  "# pinned in e4b_box.py. Round 2's log is launch2_<UTC>/chain.log\n"
  "FIRST_ROUND=3\n"),
])
edit("play_chain.want", [("de890479b92db1ea ", "3aecb6cebedd7df1 ")])
edit("precheck.sh", [
 ("[ \"$(cat \"$P/head.txt\")\" = \"37d25b6daaf3357d\" ] && say \"GATE head.txt 37d25b6daaf3357d (round 1's write, verified by the r342 one-off)\"",
  "[ \"$(cat \"$P/head.txt\")\" = \"330dd0a5dda5135e\" ] && say \"GATE head.txt 330dd0a5dda5135e (round 2's head_out, WRITE VERIFIED)\""),
 ("[ -e \"$P/round_01\" ] && [ ! -e \"$P/round_02\" ] && [ \"$(grep -c '^FIRST_ROUND=2$' \"$P/play_chain.sh\")\" = \"1\" ] && say \"GATE round_01 kept, no round_02, the chain starts at FIRST_ROUND=2\"",
  "[ -e \"$P/round_02\" ] && [ ! -e \"$P/round_03\" ] && [ \"$(grep -c '^FIRST_ROUND=3$' \"$P/play_chain.sh\")\" = \"1\" ] && say \"GATE round_02 kept, no round_03, the chain starts at FIRST_ROUND=3\""),
 ("[ ! -e \"$P/STOP\" ] && say \"GATE no STOP file\" || say \"GATE FAIL a STOP file is present\"\n",
  "[ ! -e \"$P/STOP\" ] && say \"GATE no STOP file\" || say \"GATE FAIL a STOP file is present\"\n"
  "# r355: CREDIT OFF from round 3, pinned in the box beside the seed (one line, exactly)\n"
  "[ \"$(grep -c '^os.environ\\[\"TETHER_DIVIDE_CREDIT\"\\] = \"0\"' \"$E/e4b_box.py\")\" = \"1\" ] && say \"GATE CREDIT pinned OFF in e4b_box.py (1 line)\" || say \"GATE FAIL the CREDIT pin\"\n"),
 ("run log_index_verify \"$PY\" -B harness/log_index.py verify \"C:/TETHER_RUNS/S6_2026-10-19/PLAY19/round_01/stream.jsonl\"",
  "run log_index_verify \"$PY\" -B harness/log_index.py verify \"C:/TETHER_RUNS/S6_2026-10-19/PLAY19/round_02/stream.jsonl\""),
])
print("ok")
