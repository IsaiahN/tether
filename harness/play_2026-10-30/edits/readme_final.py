import sys, hashlib
S = sys.argv[1]
cur = open(S + "/README_general.md", encoding="utf-8", newline="").read()
new1 = ("These two layers are the swappable parts. The agent decides what it intends; the layers decide how\n"
        "that is carried out, depending on the inputs and actions a world provides. The reasoning above\n"
        "them does not change with the world: a different world brings a different adapter and a\n"
        "different set of actions, and the agent's intents are carried out with whatever it provides.")
old1 = ("These two layers are where a world plugs in. The reasoning above them does not change with the\n"
        "world: a different world brings a different adapter and a different set of actions, and the\n"
        "agent's intents are carried out with whatever that world provides.")
assert cur.count(new1) == 1
base = cur.replace(new1, old1)                       # the 14:22 posted DRAFT 1
old2 = "anything learned. The agent starts from scratch. What it learns is written\n  to a lineage folder"
new2 = ("anything learned. The agent starts with its inherited library and no experience of its own.\n"
        "  What it learns is written to a lineage folder")
old3 = ("- **Priors enter under a stated rule.** A prior is admitted only if the loop cannot run without\n"
        "  it, or the agent minted a crude version first. Never because it would help on a particular\n"
        "  problem.\n")
new3 = ("- **Priors are inheritance, not answers.** The library holds human priors (atoms and\n"
        "  recipes) the agent starts with, the way an animal starts with its instincts; none is\n"
        "  written for a particular problem.\n")
fin = cur
for o, n in ((old2, new2), (old3, new3)):
    assert fin.count(o) == 1, o[:40]
    fin = fin.replace(o, n)
assert "\r" not in fin and all(ord(c) < 128 for c in fin)
open(S + "/README_general_base1422.md", "w", encoding="utf-8", newline="\n").write(base)
open(S + "/README_general_final.md", "w", encoding="utf-8", newline="\n").write(fin)
arc = open(S + "/README_arc.md", "rb").read()
open(S + "/README_arc_final.md", "wb").write(arc)
for n in ("README_general_final.md", "README_arc_final.md"):
    b = open(S + "/" + n, "rb").read()
    print(n, len(b), hashlib.sha256(b).hexdigest(), "CR" if b"\r" in b else "LF")
