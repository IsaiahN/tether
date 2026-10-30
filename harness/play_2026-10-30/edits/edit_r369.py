"""r369 in 1e's commit: the flip pair's env from ARMS/FLIPS (flip_env), not typed. argv: repo root."""
import sys

sys.dont_write_bytecode = True
R = sys.argv[1].rstrip("/")


def edit(rel, pairs):
    p = f"{R}/{rel}"
    s = open(p, encoding="utf-8", newline="").read()
    nl = "\r\n" if "\r\n" in s else "\n"
    for a, b in pairs:
        a, b = a.replace("\n", nl), b.replace("\n", nl)
        assert s.count(a) == 1, (rel, a[:80], s.count(a))
        s = s.replace(a, b)
    open(p, "w", encoding="utf-8", newline="").write(s)


edit("tests/_batch.py", [
 ("    for flipped, last, before, _c in FLIPS:\n"
  "        if flipped not in env and i <= names.index(last):\n"
  "            env[flipped] = before\n"
  "    return env\n",
  "    for flipped, last, before, _c in FLIPS:\n"
  "        if flipped not in env and i <= names.index(last):\n"
  "            env[flipped] = before\n"
  "    return env\n\n\n"
  "def flip_env(flipped: str) -> dict:\n"
  "    \"\"\"A flip's own identity against the tree before it (r369): the flipped arm at its value\n"
  "    before the flip, and every batch arm that landed after the flip OFF.\"\"\"\n"
  "    names = [a for a, _c in ARMS]\n"
  "    (_f, last, before, _c), = [f for f in FLIPS if f[0] == flipped]\n"
  "    return {flipped: before, **dict.fromkeys(names[names.index(last) + 1:], \"0\")}\n"),
])
edit("tests/test_divide.py", [
 ("from _batch import off_env",
  "from _batch import flip_env, off_env"),
 ("def check_credit_flip_identity_grid() -> None:\n"
  "    _off_identity(\"grid\", FLIP_BASE, \"TETHER_DIVIDE_CREDIT\", {\"TETHER_DIVIDE_CREDIT\": \"1\"})\n",
  "def check_credit_flip_identity_grid() -> None:\n"
  "    _off_identity(\"grid\", FLIP_BASE, \"TETHER_DIVIDE_CREDIT\", flip_env(\"TETHER_DIVIDE_CREDIT\"))\n"),
 ("def check_credit_flip_identity_fake() -> None:\n"
  "    _off_identity(\"fake\", FLIP_BASE, \"TETHER_DIVIDE_CREDIT\", {\"TETHER_DIVIDE_CREDIT\": \"1\"})\n",
  "def check_credit_flip_identity_fake() -> None:\n"
  "    _off_identity(\"fake\", FLIP_BASE, \"TETHER_DIVIDE_CREDIT\", flip_env(\"TETHER_DIVIDE_CREDIT\"))\n"),
])
print("ok")
