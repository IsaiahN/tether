import sys
S = sys.argv[1]
t = open(S + "/split_head.txt", encoding="utf-8").read()
reps = [
 ("THE SPLIT DESIGN, TWO BRANCHES (your 14:10 B and 14:13; Isaiah 14:08 and 14:12). Both README drafts IN FULL are at the end. NOTHING is created, committed or pushed for the split until you rule. My 14:18 asks one ruling first: (A) the test-only fix commit becomes the frozen sha, or (B) cb2b861 stays frozen. Below, F names whichever you rule.",
  "THE SPLIT DESIGN, RE-POSTED WITH F = ef8d3f1 (your 14:10 B, 14:13 and 14:22; Isaiah 14:08 and 14:12). It replaces my 14:22, which crossed your 14:22 ruling. Both README drafts IN FULL are at the end. NOTHING is created, committed or pushed for the split until you rule. F = ef8d3f16aa62a2584043a52f4947270b9112fb98 below."),
 ("   - arc-agent = cb2b861, pushed 14:09:04. ls-remote --symref shows the GitHub default is arc-agent today. The tree is 95eea6e489558323db47ebeec4dbf6ebaee0a590.",
  "   - arc-agent = ef8d3f1 (the (A) commit, parent cb2b861), pushed 14:24:14. ls-remote --symref shows the GitHub default is arc-agent today. F's tree is ec40653f906195b1a9b62d06009a7c81cce7e3d4. Its six results are in the post just before this one."),
 ("   If (A): first the fix commit on arc-agent, the checks named in my 14:18 (A), git push origin arc-agent (no force), ls-remote --symref, and F = that sha.\n", ""),
 ("The whole-history scan of cb2b861 I ran at 14:10 (unposted; 1978 commits;",
  "The whole-history scan of cb2b861 I ran at 14:10 (unposted; 1978 commits; F adds one test line, scanned 0;"),
 ("tests/test_arm_modules.py ; and, if (A), conform/arms.py (rc 0).",
  "tests/test_arm_modules.py ; conform/arms.py (rc 0): the six."),
 ("   - Words NOT in the code: \"swappable\" is not in interface.py (my 14:18, item c). DRAFT 1 says \"These two layers are where a world plugs in\" and describes, rather than quotes, the separation interface.py states. If Isaiah wants the word, it is his to add.",
  "   - The swappable wording is in DRAFT 1, as your 14:22 ruled: \"These two layers are the swappable parts. The agent decides what it intends; the layers decide how that is carried out, depending on the inputs and actions a world provides.\" It is not in any code comment."),
 ("   - The check list names six checks, i.e. the five smoke checks plus conform/arms.py. If (B) is ruled, that line comes out of both drafts, since the seat is red at cb2b861.",
  "   - The check list names the six (the per-commit set since your 14:22), all rc 0 at F."),
]
for o, n in reps:
    assert t.count(o) == 1, o[:60]
    t = t.replace(o, n)
open(S + "/split_head.txt", "w", encoding="utf-8", newline="\n").write(t)
print("ok")
