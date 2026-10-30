import sys
S = sys.argv[1]
head = open(S + "/split_head.txt", encoding="utf-8").read()
g = open(S + "/README_general.md", encoding="utf-8").read()
a = open(S + "/README_arc.md", encoding="utf-8").read()
out = (head + "\n==================== DRAFT 1: README.md on general-agent (in full) ====================\n"
       + g + "==================== END DRAFT 1 ====================\n"
       + "\n==================== DRAFT 2: README.md on arc-solver-agent (in full) ====================\n"
       + a + "==================== END DRAFT 2 ====================\n")
open(S + "/post_split2.txt", "w", encoding="utf-8", newline="\n").write(out)
print(len(out), sum(1 for ch in out if ord(ch) > 127))
