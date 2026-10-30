import sys
from pathlib import Path
sys.dont_write_bytecode = True
p = Path(sys.argv[1]); s = p.read_text(encoding="utf-8")
R = [("import collections\nimport hashlib\n", "import collections\nimport glob\nimport hashlib\n"),
     ('GAMES = tuple(sys.argv[3:]) or ("g50t", "ka59", "r11l", "sb26", "su15", "tr87", "ft09")\n',
      'GAMES = tuple(sys.argv[3:]) or ("g50t", "ka59", "r11l", "sb26", "su15", "tr87", "ft09")\n'
      'E4A = "C:/TETHER_RUNS/E4_2026-10-18/public"\n'),
     ("          traceback.txt; the load read the point's head (load_report.json lineage_parent = the manifest's one generation\n"
      "          no other names as parent)\n",
      "          traceback.txt; the load read the last verified head (load_report.json lineage_parent = write_check.json's\n"
      "          head_in: the S3O point's head for the first game, the previous game's verified tip after it)\n"),
     ("  WRITE   the result row (result.json readable, with game, agent_steps, lineage); the generations the copy gained (not in\n"
      "          the manifest), each decoded; their chain starts at the point's head and ends at the generation result.json names;\n"
      "          every manifest file other than memory.db* unchanged on the copy (sha256), memory.db* named if it changed\n",
      "  WRITE   the result row (result.json readable, with game, agent_steps, lineage) and pf_check's write_check.json\n"
      "          (VERIFIED, head in, chain, names added, why). The REAL lineage is never read here (the reviewer 00:20 (i));\n"
      "          only pf_check reads it, by bytes. (Rewritten 2026-10-23 02:15 from a per-game-copy reader.)\n"
      "  E4A     the same game's E4a row (public/NN_<game>/<game>.result.json, else its sup.json) for the pace\n"),
     ]
for a, b in R:
    assert s.count(a) == 1, a[:60]
    s = s.replace(a, b)
p.write_text(s, encoding="utf-8", newline="\n"); print("ok")
