"""(a2): TETHER_DIVIDE_CREDIT's tree default flipped to OFF (Isaiah 2026-10-29 15:50; r344, r355, r359), the
FLIPS table in tests/_batch.py, and the flip's own identity in test_divide. argv: repo root."""
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


edit("tether.py", [
 ("# never met. Its cost is in the other currency (wall), read apart. Needs TETHER_DIVIDE. ON;\n"
  "# conform/arms.py\n"
  "_DIVIDE_CREDIT = armflag.arm(\"TETHER_DIVIDE_CREDIT\", default=True)\n",
  "# never met. Its cost is in the other currency (wall), read apart. Needs TETHER_DIVIDE. OFF since\n"
  "# (a2) (Isaiah 2026-10-29 15:50 \"you can switch off credit\"; r344, r355): the yield is refunded\n"
  "# but not the work. conform/arms.py\n"
  "_DIVIDE_CREDIT = armflag.arm(\"TETHER_DIVIDE_CREDIT\", default=False)\n"),
])

edit("conform/arms.py", [
 ("                            \"'credited'. Its cost is wall time, read apart from DIVIDE's. OFF: no \"\n"
  "                            \"credit is written and the closure counts as before. default ON\",\n",
  "                            \"'credited'. Its cost is wall time, read apart from DIVIDE's. OFF: no \"\n"
  "                            \"credit is written and the closure counts as before. default OFF since \"\n"
  "                            \"(a2): the credit refunds the yield count but not the work, so a \"\n"
  "                            \"credited walk runs the whole space (r344's ledger read: credited = \"\n"
  "                            \"candidates_seen = 62,585 on a PLAY19 round-1 walk); Isaiah 2026-10-29 \"\n"
  "                            \"15:50 'you can switch off credit' (r355). ON is a measuring setting\",\n"),
])

edit("tests/_batch.py", [
 ("    (\"TETHER_STOP_RULES\", None),             # 1c; its sha comes with the next arm\n"
  ")\n",
  "    (\"TETHER_STOP_RULES\", \"d148097\"),        # 1c\n"
  ")\n"
  "# A batch arm whose TREE DEFAULT was flipped after later arms landed (r359): (the arm, the last batch\n"
  "# arm before the flip, its value before, the flip's commit). An arm under test that landed after the\n"
  "# flipped arm and up to the flip was gated against bases holding the old value, so off_env pins it.\n"
  "FLIPS = (\n"
  "    (\"TETHER_DIVIDE_CREDIT\", \"TETHER_STOP_RULES\", \"1\", None),   # (a2), Isaiah 2026-10-29 15:50\n"
  ")\n"),
 ("    \"\"\"The arm and every later batch arm OFF, for an OFF identity against the arm's base.\"\"\"\n"
  "    names = [a for a, _c in ARMS]\n"
  "    assert arm in names, (\"not a batch arm\", arm)\n"
  "    return dict.fromkeys(names[names.index(arm):], \"0\")\n",
  "    \"\"\"The arm and every later batch arm OFF, for an OFF identity against the arm's base; a flipped\n"
  "    arm that landed before it is pinned to its value before the flip (FLIPS).\"\"\"\n"
  "    names = [a for a, _c in ARMS]\n"
  "    assert arm in names, (\"not a batch arm\", arm)\n"
  "    i = names.index(arm)\n"
  "    env = dict.fromkeys(names[i:], \"0\")\n"
  "    for flipped, last, before, _c in FLIPS:\n"
  "        if flipped not in env and i <= names.index(last):\n"
  "            env[flipped] = before\n"
  "    return env\n"),
])

edit("tests/test_divide.py", [
 ("  check_credit_off_identity_grid, check_credit_off_identity_fake   TETHER_DIVIDE_CREDIT=0 writes\n"
  "                      the same ledger as d6a4055 (1b)\n",
  "  check_credit_off_identity_grid, check_credit_off_identity_fake   TETHER_DIVIDE_CREDIT=0 writes\n"
  "                      the same ledger as d6a4055 (1b)\n"
  "  check_credit_flip_identity_grid, check_credit_flip_identity_fake   (a2): this tree with\n"
  "                      TETHER_DIVIDE_CREDIT=1 writes the same ledger as d148097, the tree before the\n"
  "                      default flip\n"),
 ("def _off_identity(w: str, base_tree: str = BASE, arm: str = \"TETHER_DIVIDE\") -> None:\n",
  "def _off_identity(w: str, base_tree: str = BASE, arm: str = \"TETHER_DIVIDE\",\n"
  "                  env: dict | None = None) -> None:\n"),
 ("    cur = norm(_child(root, w, off_env(arm)))\n",
  "    env = off_env(arm) if env is None else env\n"
  "    cur = norm(_child(root, w, env))\n"),
 ("    print(f\"  OFF identity ({arm}=0, {w}): {len(base)} rows against {base_tree}, 0 differences\")\n",
  "    print(f\"  identity ({', '.join(f'{k}={v}' for k, v in sorted(env.items()))}, {w}): \"\n"
  "          f\"{len(base)} rows against {base_tree}, 0 differences\")\n"),
 ("def check_credit_off_identity_fake() -> None:\n"
  "    _off_identity(\"fake\", CREDIT_BASE, \"TETHER_DIVIDE_CREDIT\")\n",
  "def check_credit_off_identity_fake() -> None:\n"
  "    _off_identity(\"fake\", CREDIT_BASE, \"TETHER_DIVIDE_CREDIT\")\n"
  "\n"
  "\n"
  "FLIP_BASE = \"d148097\"      # 1c, the tree before (a2) flipped CREDIT's default to OFF\n"
  "\n"
  "\n"
  "def check_credit_flip_identity_grid() -> None:\n"
  "    _off_identity(\"grid\", FLIP_BASE, \"TETHER_DIVIDE_CREDIT\", {\"TETHER_DIVIDE_CREDIT\": \"1\"})\n"
  "\n"
  "\n"
  "def check_credit_flip_identity_fake() -> None:\n"
  "    _off_identity(\"fake\", FLIP_BASE, \"TETHER_DIVIDE_CREDIT\", {\"TETHER_DIVIDE_CREDIT\": \"1\"})\n"),
])
print("ok")
