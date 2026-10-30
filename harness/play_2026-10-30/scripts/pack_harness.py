"""r447 item 3: copy the harness / reader / edit-tool files byte-identical into a destination folder and write
MANIFEST.tsv (class, published path, source path, sha256, bytes). Class is by the rule below, by file name; only the
PLAY set (E4B_SPY, PF/pf_check.py, PLAY24's five) is checked against what PLAY24 pins. Each copy is re-hashed after.
argv: dest folder (harness/play_2026-10-30 in the new worktree), drafts folder (for AGENT test drafts), list file."""
import hashlib
import os
import re
import shutil
import sys

sys.dont_write_bytecode = True
DEST, DRAFTS, LST = sys.argv[1], sys.argv[2], sys.argv[3]
R = "/c/TETHER_RUNS/S6_2026-10-19/"
HARNESS = re.compile(r"^(auto_play\d+.*\.ps1|want\d+\.sh|carry24\.py|make_play\d+\.py|backup_lineage\.py|backup_rundir\.py"
                     r"|relaunch3\.py|spy_sweep\.py|inv_git\.sh|.*_run\.sh|run_.*\.sh|round16\.sh|abc2?\.sh|act_runs\.sh"
                     r"|mint_runs\.sh|prof.*\.sh|set_fd\.sh|stop_smoke\.sh|pack_harness\.py)$")
DRAFT = re.compile(r"^(test_.*\.py|1c_test_stop_rules\.py)$")
EDIT = re.compile(r"(edit|fix|patch|^ledger_|^readme_|wrap|^place_test|splice|cut_lines|crlf|^fill|^tw_head|^resolve_1c"
                  r"|^drop8th|^split_a1|^mk_split|^mk_r2|^item\d|^commit1|^s0_doc|^repo_doc|^c2_ledger)")


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


rows = []
for src in open(LST, encoding="utf-8").read().split():
    src = src if src.startswith("/") else os.path.join(os.path.dirname(LST), src)
    name = os.path.basename(src)
    if src.startswith(R):
        cls, rel = "HARNESS-PLAY", os.path.join("play", src[len(R):])
        base = DEST
        src = "C:/" + src[3:]
    elif DRAFT.match(name):
        cls, rel, base = "AGENT-TEST-DRAFT", name, DRAFTS
    elif HARNESS.match(name):
        cls, rel, base = "HARNESS", os.path.join("scripts", name), DEST
    elif EDIT.search(name):
        cls, rel, base = "EDIT-TOOL", os.path.join("edits", name), DEST
    else:
        cls, rel, base = "READER", os.path.join("readers", name), DEST
    dst = os.path.join(base, rel)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copyfile(src, dst)
    h = sha(src)
    assert sha(dst) == h, dst
    rows.append((cls, rel.replace(os.sep, "/"), src, h, os.path.getsize(src), base))
for base in (DEST, DRAFTS):
    with open(os.path.join(base, "MANIFEST.tsv"), "w", encoding="utf-8", newline="\n") as f:
        f.write("# class\tpath (in this folder)\tsource on the box\tsha256\tbytes\n")
        for cls, rel, src, h, n, b in sorted(rows, key=lambda r: (r[0], r[1])):
            if b == base:
                f.write(f"{cls}\t{rel}\t{src}\t{h}\t{n}\n")
counts = {}
for r in rows:
    counts[r[0]] = counts.get(r[0], 0) + 1
print("copied", len(rows), "verified;", counts)
