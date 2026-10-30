"""Write PLAY19's chain, precheck, want and play_across.py from PLAY18's, each change asserted to land
exactly once. argv: PLAY18 dir, PLAY19 dir, the 16-hex head PLAY19 starts from, a short note."""
import hashlib
import shutil
import sys

sys.dont_write_bytecode = True
src_dir, dst_dir, head, note = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
assert len(head) == 16 and all(c in "0123456789abcdef" for c in head), head
G = "dad9d2b06a96b50a7426c0360df5e6eb51d14236"
H = "8412f6f4540d816bf6f1f0073bb4d2bb557109c9"
E = "C:/TETHER_RUNS/S6_2026-10-19/E4B_SPY"
CHK = "C:/TETHER_RUNS/S6_2026-10-19/PF/pf_check.py"
T = "C:/TETHER_RUNS/S6_2026-10-19/split/fresh_r25/arc-solver-agent"


def edit(text, pairs):
    for old, new in pairs:
        assert text.count(old) == 1, (text.count(old), old[:80])
        text = text.replace(old, new)
    return text


common = [
    ('P="C:/TETHER_RUNS/S6_2026-10-19/PLAY18"', 'P="C:/TETHER_RUNS/S6_2026-10-19/PLAY19"'),
    ('T="C:/TETHER_RUNS/S6_2026-10-19/split/fresh_r24/arc-solver-agent"', f'T="{T}"'),
    ("G=549f403e220cbaadb392c4639ffe7887c6ef2575", f"G={G}"),
    ("H=45234bab4f23bbedd3ee79bcea0fd56c5a3793af", f"H={H}"),
    # r319 step 4: arc_atoms.py changed in 1b, hashed by name beside the others
    ('"$T/gamma.py" "$T/lineage.py" | cut -c1-16',
     '"$T/gamma.py" "$T/lineage.py" "$T/arc_atoms.py" | cut -c1-16'),
]

chain = open(f"{src_dir}/play_chain.sh", encoding="utf-8", newline="").read()
chain = edit(chain, common + [
    ("#!/bin/bash\n",
     "#!/bin/bash\n# PLAY19 = PLAY18 on the NEW tree: arc-solver-agent 8412f6f (general-agent dad9d2b, decision\n"
     "# 1a: TETHER_DIVIDE, TETHER_DIVIDE_CREDIT, + README), a fresh clone split/fresh_r25 with M3\n"
     f"# (the reviewer r319), the same E4B_SPY box; from {head[:8]} ({note}).\n"
     "# Open-ended; the STOP file is the exit.\n"),
])
open(f"{dst_dir}/play_chain.sh", "w", encoding="utf-8", newline="").write(chain)

pre = open(f"{src_dir}/precheck.sh", encoding="utf-8", newline="").read()
pre = edit(pre, common + [
    ('[ "$(cat "$P/head.txt")" = "f6e42d42a20bc264" ] && say "GATE head.txt f6e42d42a20bc264" || say "GATE FAIL head.txt"',
     f'[ "$(cat "$P/head.txt")" = "{head}" ] && say "GATE head.txt {head}" || say "GATE FAIL head.txt"'),
])
open(f"{dst_dir}/precheck.sh", "w", encoding="utf-8", newline="").write(pre)
shutil.copyfile(f"{src_dir}/play_across.py", f"{dst_dir}/play_across.py")
open(f"{dst_dir}/head.txt", "w", encoding="utf-8", newline="").write(head + "\n")

files = [f"{E}/e4b_box.py", f"{E}/e4b_run.py", f"{E}/e4b_read.py", f"{E}/break_audit.py", CHK,
         f"{T}/harness/mem_store/e4_stream.py", f"{T}/tether.py", f"{T}/harness/log_index.py",
         f"{dst_dir}/play_across.py", f"{T}/arc_percept.py", f"{T}/arc_world.py",
         f"{T}/conform/arms.py", f"{T}/gamma.py", f"{T}/lineage.py", f"{T}/arc_atoms.py"]
want = " ".join(hashlib.sha256(open(p, "rb").read()).hexdigest()[:16] for p in files)
open(f"{dst_dir}/play_chain.want", "w", encoding="utf-8", newline="").write(want + "\n")
print("written; want", want)
