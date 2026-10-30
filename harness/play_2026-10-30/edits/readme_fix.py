import sys
S = sys.argv[1]
g = open(S + "/README_general.md", encoding="utf-8").read()
a = open(S + "/README_arc.md", encoding="utf-8").read()
old_g = ("agent's intents are carried out with whatever that world provides. This branch carries a\n"
         "symbolic world (`world.py`) and a grid world (`gridworld.py`).")
new_g = ("agent's intents are carried out with whatever that world provides. The tree carries a\n"
         "symbolic world (`world.py`), a grid world (`gridworld.py`), and the ARC-AGI-3 adapter and\n"
         "harness, which are identical on both branches (see `arc-solver-agent`'s README).")
old_env = "    set PYTHONDONTWRITEBYTECODE=1                       # export ... off Windows\n"
new_env = "    export PYTHONDONTWRITEBYTECODE=1                    # a POSIX shell; Git Bash on Windows\n"
old_a = ("- **The agent is told nothing about a game** beyond what it perceives: no game name, no goal, no\n"
         "  rules. Nothing it decides reads a game's identity.")
new_a = ("- **The agent is told nothing about a game** beyond what it perceives: no goal and no rules. By\n"
         "  the project's standing rule, no decision may read a game's identity.")
for s, o, n in ((g, old_g, new_g), (g, old_env, new_env), (a, old_a, new_a)):
    assert s.count(o) == 1, o[:40]
g = g.replace(old_g, new_g).replace(old_env, new_env)
a = a.replace(old_a, new_a)
open(S + "/README_general.md", "w", encoding="utf-8", newline="\n").write(g)
open(S + "/README_arc.md", "w", encoding="utf-8", newline="\n").write(a)
print("ok")
