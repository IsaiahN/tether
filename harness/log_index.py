import sys

sys.dont_write_bytecode = True   # first, before any other import (Isaiah 10-17 05:01)
# ruff: noqa: E402 -- every import follows the bytecode switch above
"""THE LOG INDEX, L4 (Isaiah 2026-10-14 19:05, 2026-10-20 05:01; the reviewer 2026-10-21 23:27,
2026-10-22 00:03). Seat side: the agent never imports this, and it never reads or writes a lineage,
a memory.db or a library. One summary row per run ledger, appended to an index that only grows (Fig
6 :42); a ledger may be retired only once its row is RECOMPUTED from it and found equal (Fig 4
:30-32, the round trip), outside the window of the 25 newest and not pinned, and with Isaiah's own
approval. The row is lossy by design and says what it dropped (Fig 4 :27-31).

    python -B harness/log_index.py add ROOT... [--budget-s S]    index ledgers not yet indexed
    python -B harness/log_index.py verify PATH...                recompute, compare; exit 1 on any
    python -B harness/log_index.py pins SOURCE... [--check]      generate the pins from the record
    python -B harness/log_index.py window ROOT... [--verify]     list the eligible; removes nothing
    python -B harness/log_index.py retire LIST --approval TEXT --roots ROOT...
                                                    rename each to .dead-<UTC>, logged

Options: --index, --pins, --removals (defaults beside each other in the runs folder,
TETHER_RUNS_DIR, which has no default: unset, any command that needs it stops and names it). A
ledger is a
*.jsonl whose first row has "step" and "event" (the tombstone's rule, docs/TOMBSTONES). Nothing here
deletes: the .dead files are removed as a separate, ruled step. The pins' sources are the record:
docs/*.md, the repo's *.py and tests/*.py less tests/test_log_index.py (its planted S9Z),
harness/*.py, conform/*.py;
hand rows (an alias, a whole root) are kept from the pins file. The index, the pins and the
removals are run output: kept locally and never committed (Isaiah 2026-10-30 16:33, superseding the
reviewer's 2026-10-22 00:03 A copy under docs/log_index/). The box folders are scanned under the
runs folder and under the holding folder beside it (TETHER_HOLDING_DIR, else the runs folder's
sibling TETHER_HOLDING).
"""
import argparse
import hashlib
import json
import os
import re
import time
from pathlib import Path


def home() -> Path:
    """The runs folder: TETHER_RUNS_DIR, with no machine default (Isaiah 2026-10-30 16:33)."""
    d = os.environ.get("TETHER_RUNS_DIR")
    if not d:
        raise SystemExit("log_index: set TETHER_RUNS_DIR to the runs folder")
    return Path(d)


WINDOW = 25   # the newest ledgers kept full (the reviewer 2026-10-22 00:03 (a): globally, by mtime)
# a box is cited by its folder's name: the folders directly under a dated run root (BOX_PARENTS'
# children), and any token of a citation pattern -- an S box, or a worktree (wt_..., tether-wt...;
# the reviewer 2026-10-22 00:30 (c)) -- which must then resolve to a folder or a hand row (MF6)
BOX_RE = re.compile(r"\bS[0-9][A-Z]{1,2}\b|\bwt_[A-Za-z0-9_]+|\btether-wt[-A-Za-z0-9]*")
def box_parents() -> tuple[str, str]:
    hold = os.environ.get("TETHER_HOLDING_DIR") or str(home().parent / "TETHER_HOLDING")
    return (home().as_posix() + "/*", Path(hold, "2026-10-16_step7_runs").as_posix())


KEPT_SLOTS = ("@run", "@boundary", "@loop")
DROPPED = "every other row's detail (each kind's count and first/last cycle are in tally)"
SUMMARISER = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()[:16]


def norm(p) -> str:
    return str(p).replace("\\", "/")


def is_ledger(p: Path) -> bool:
    if p.suffix != ".jsonl" or p.name.endswith(".body.jsonl"):
        return False
    try:
        with open(p, "rb") as f:
            r = json.loads(f.readline())
    except (OSError, ValueError):
        return False
    return isinstance(r, dict) and "step" in r and "event" in r


def ledgers(roots) -> list[Path]:
    out = []
    for r in roots:
        for d, dirs, names in os.walk(r):
            dirs[:] = [x for x in dirs if x not in (".git", ".venv", "venv")
                       and not os.path.islink(os.path.join(d, x))]
            out += [p for n in names if (p := Path(d) / n).suffix == ".jsonl" and is_ledger(p)]
    return out


def header(d: dict) -> dict:
    keep = ("head", "tree", "dirty", "files_sha", "library_sha", "library", "game", "world",
            "entry", "seed", "generation", "on", "off")
    on, off = sorted(d.get("on", ())), sorted(d.get("off", ()))
    sha = hashlib.sha256(json.dumps([on, off]).encode()).hexdigest()[:16]
    return {**{k: d.get(k) for k in keep}, "n_on": len(on), "n_off": len(off), "arms_sha": sha}


def summarise(p: Path) -> dict:
    """The row, read only from the ledger and its result.json sidecar, with no interpretation."""
    st = p.stat()
    h = hashlib.sha256()
    rows = bad = 0
    tally: dict[str, list] = {}
    kept, hdr, seq, maxc = [], None, [None, None], None
    with open(p, "rb") as f:
        for raw in f:
            h.update(raw)
            rows += 1
            try:
                r = json.loads(raw)
            except ValueError:
                bad += 1
                continue
            if not isinstance(r, dict):
                bad += 1
                continue
            c, ev, slot = r.get("cycle"), r.get("event"), r.get("slot")
            t = tally.setdefault(f"{r.get('step')}|{ev}", [0, c, c])
            t[0] += 1
            t[2] = c
            if seq[0] is None:
                seq[0] = r.get("seq")
            seq[1] = r.get("seq")
            if isinstance(c, int) and (maxc is None or c > maxc):
                maxc = c
            if slot == "@run" and ev == "arms" and hdr is None:
                hdr = header(r.get("detail") or {})
                continue
            if slot in KEPT_SLOTS or ev == "ending" or str(ev).endswith("_end"):
                kept.append(r)
    side = p.with_name(p.name[:-len(".jsonl")] + ".result.json")
    try:
        result = json.loads(side.read_text(encoding="utf-8")) if side.is_file() else None
    except (OSError, ValueError):
        result = {"unreadable": side.name}
    return {"path": norm(p), "bytes": st.st_size, "mtime": st.st_mtime, "sha256": h.hexdigest(),
            "rows": rows, "bad": bad, "seq": seq, "max_cycle": maxc, "header": hdr,
            "tally": tally, "kept_rows": kept, "result": result, "dropped": DROPPED,
            "summariser": SUMMARISER}


def load_index(path: Path) -> dict[str, dict]:
    """path -> its LAST row (a re-index appends; nothing is rewritten)."""
    out: dict[str, dict] = {}
    if path.is_file():
        with open(path, encoding="utf-8") as f:
            for n, line in enumerate(f, 1):
                r = json.loads(line)
                r["_line"] = n
                out[r["path"].lower()] = r
    return out


def same(row: dict, fresh: dict) -> list[str]:
    """The fields that differ between a stored row and one recomputed now. indexed_at and the
    summariser stamp aside: the stamp is the sha of this whole file, so it names the provenance of
    the row and moves with any edit here; the round trip is the content."""
    skip = ("indexed_at", "_line", "summariser")
    a = {k: v for k, v in row.items() if k not in skip}
    b = {k: v for k, v in json.loads(json.dumps(fresh)).items() if k not in skip}
    return sorted(k for k in set(a) | set(b) if a.get(k) != b.get(k))


def cmd_add(a) -> int:
    idx = load_index(a.index)
    t0, done, skipped = time.time(), 0, 0
    with open(a.index, "a", encoding="utf-8") as out:
        for p in ledgers(a.roots):
            old = idx.get(norm(p).lower())
            st = p.stat()
            if old and old["bytes"] == st.st_size and old["mtime"] == st.st_mtime:
                skipped += 1
                continue
            if a.budget_s and time.time() - t0 > a.budget_s:
                print(f"BUDGET: stopped after {done} indexed; resume with the same command")
                break
            row = summarise(p)
            row["indexed_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            out.write(json.dumps(row, sort_keys=True) + "\n")
            out.flush()
            os.fsync(out.fileno())
            done += 1
            print(f"{time.time() - t0:8.1f}s {row['bytes']:>12,} B {row['rows']:>9,} rows {p}",
                  flush=True)
    print(f"ADD: {done} indexed, {skipped} already indexed, {time.time() - t0:.1f} s")
    return 0


def verify_one(idx: dict, p: Path) -> list[str]:
    row = idx.get(norm(p).lower())
    if row is None:
        return ["not indexed"]
    if not p.is_file():
        return ["missing on disk"]
    return same(row, summarise(p))


def cmd_verify(a) -> int:
    idx, bad = load_index(a.index), 0
    for p in map(Path, a.paths):
        d = verify_one(idx, p)
        bad += bool(d)
        print(("REFUSED " + ",".join(d) if d else "OK") + f"  {norm(p)}")
    return 1 if bad else 0


def read_pins(path: Path) -> list[tuple[str, str]]:
    if not path.is_file():
        return []
    rows = [ln.split("\t") for ln in path.read_text(encoding="utf-8").splitlines()]
    return [(r[0], r[1] if len(r) > 1 else "") for r in rows if r and r[0] and r[0][0] != "#"]


def pinned(p: str, pins) -> str | None:
    lo = p.lower()
    return next((why for pre, why in pins if lo.startswith(pre.lower().rstrip("/") + "/")
                 or lo == pre.lower()), None)


def box_folders() -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    for pat in box_parents():
        base = Path(pat.removesuffix("/*"))
        parents = sorted(d for d in base.iterdir() if d.is_dir()) if pat.endswith("/*") else [base]
        for parent in parents:
            for d in sorted(parent.iterdir()):
                if d.is_dir():
                    out.setdefault(d.name, []).append(norm(d))
    return out


def gen_pins(sources: list[Path], folders: dict[str, list[str]], hand) -> tuple[list, list]:
    """(generated pins, unresolved citations). A folder is pinned when a source (the LEDGER, the
    repo's docs and code) names it as a whole token; a box-pattern token must resolve to a folder
    or a hand pin, or it is unresolved."""
    text = " ".join(s.read_text(encoding="utf-8", errors="replace") for s in sources)
    words = set(re.findall(r"[A-Za-z0-9_.\-]+", text))
    gen = [(f, f"cited: {name}") for name, fs in sorted(folders.items()) if name in words
           for f in fs]
    # a hand row resolves the citation tokens its reason names before " ran " (an alias names
    # the folder it ran in after it); a row for a token with no folder resolves it as absent
    hand_names = {b for _pre, why in hand for b in BOX_RE.findall(why.split(" ran ")[0])}
    unresolved = sorted(b for b in set(BOX_RE.findall(text))
                        if b not in folders and b not in hand_names)
    return gen, unresolved


def cmd_pins(a) -> int:
    hand = [(pre, why) for pre, why in read_pins(a.pins) if not why.startswith("cited: ")]
    gen, unresolved = gen_pins([Path(s) for s in a.sources], box_folders(), hand)
    want = sorted(set(gen) | set(hand))
    have = sorted(set(read_pins(a.pins)))
    for u in unresolved:
        print(f"UNRESOLVED: {u} is cited and resolves to no folder or hand pin")
    if a.check:
        miss = sorted(set(want) - set(have))
        for m in miss:
            print(f"MISSING PIN: {m[0]}\t{m[1]}")
        ok = not miss and not unresolved
        print(f"PINS {'OK' if ok else 'FAIL'}: {len(have)} pinned, {len(miss)} missing, "
              f"{len(unresolved)} unresolved")
        return 0 if ok else 1
    with open(a.pins, "w", encoding="utf-8", newline="\n") as f:
        f.write("# prefix\treason (generated by harness/log_index.py pins; hand rows kept)\n")
        for pre, why in want:
            f.write(f"{pre}\t{why}\n")
    print(f"PINS WRITTEN: {len(want)} ({len(gen)} generated, {len(hand)} hand), "
          f"{len(unresolved)} unresolved")
    return 1 if unresolved else 0


def eligible(idx: dict, found: list[Path], pins, verify: bool) -> tuple[list, list]:
    newest = sorted(found, key=lambda p: p.stat().st_mtime, reverse=True)[:WINDOW]
    win = {norm(p).lower() for p in newest}
    out, held = [], []
    for p in found:
        k = norm(p).lower()
        why = ("window" if k in win else pinned(norm(p), pins)
               or (None if k in idx else "not indexed"))
        if why is None and verify and (d := verify_one(idx, p)):
            why = "verify: " + ",".join(d)
        (held if why else out).append((p, why))
    return out, held


def cmd_window(a) -> int:
    idx, pins = load_index(a.index), read_pins(a.pins)
    out, held = eligible(idx, ledgers(a.roots), pins, a.verify)
    per: dict[str, list] = {}
    for p, _ in out:
        v = per.setdefault(norm(p.parent), [0, 0])
        v[0] += 1
        v[1] += p.stat().st_size
    for d, (n, b) in sorted(per.items(), key=lambda kv: -kv[1][1]):
        print(f"ELIGIBLE {n:5} {b / 2**20:10.1f} MB  {d}")
    reasons: dict[str, int] = {}
    for _, why in held:
        k = why.split(":")[0] if why.startswith("verify") else why
        reasons[k] = reasons.get(k, 0) + 1
    print(f"WINDOW: {len(out)} eligible ({sum(p.stat().st_size for p, _ in out) / 2**30:.2f} GiB)"
          f" {'verified' if a.verify else 'NOT verified'}; held {len(held)}: {reasons}")
    if a.out:
        Path(a.out).write_text("".join(norm(p) + "\n" for p, _ in out), encoding="utf-8")
    return 0


def cmd_retire(a) -> int:
    if not a.approval.strip():
        print("REFUSED: retire needs Isaiah's own approval text (--approval)")
        return 1
    idx, pins = load_index(a.index), read_pins(a.pins)
    paths = [Path(x.strip()) for x in Path(a.list).read_text(encoding="utf-8").splitlines()
             if x.strip()]
    # the window is the newest 25 of EVERY ledger under the roots, never of the list alone;
    # the round trip is read for the list's members only (the roots hold ~32 GiB)
    ok, held = eligible(idx, ledgers(a.roots), pins, verify=False)
    ok_set = {norm(p).lower() for p, _ in ok}
    refused = [(p, dict(held).get(p, "not eligible")) for p in paths
               if norm(p).lower() not in ok_set]
    refused += [(p, "verify: " + ",".join(d)) for p in paths
                if norm(p).lower() in ok_set and (d := verify_one(idx, p))]
    if refused:
        for p, why in refused:
            print(f"REFUSED {why}  {norm(p)}")
        print(f"RETIRE REFUSED: {len(refused)} of {len(paths)}; nothing renamed")
        return 1
    utc = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    with open(a.removals, "a", encoding="utf-8", newline="\n") as log:
        for p in paths:
            row = idx[norm(p).lower()]
            dead = p.with_name(p.name + f".dead-{utc}")
            os.replace(p, dead)
            log.write("\t".join([utc, norm(p), norm(dead), str(row["bytes"]), row["sha256"],
                                 str(row["_line"]), a.approval.replace("\t", " ")]) + "\n")
            print(f"RETIRED {norm(p)} -> {dead.name}")
    print(f"RETIRE: {len(paths)} renamed; LOG_REMOVALS {norm(a.removals)}")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--index", type=Path)
    ap.add_argument("--pins", type=Path)
    ap.add_argument("--removals", type=Path)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("add")
    s.add_argument("roots", nargs="+")
    s.add_argument("--budget-s", type=float, default=0)
    s = sub.add_parser("verify")
    s.add_argument("paths", nargs="+")
    s = sub.add_parser("pins")
    s.add_argument("sources", nargs="+")
    s.add_argument("--check", action="store_true")
    s = sub.add_parser("window")
    s.add_argument("roots", nargs="+")
    s.add_argument("--verify", action="store_true")
    s.add_argument("--out")
    s = sub.add_parser("retire")
    s.add_argument("list")
    s.add_argument("--approval", required=True)
    s.add_argument("--roots", nargs="+", required=True)
    a = ap.parse_args(argv)
    for k, name in (("index", "LOG_INDEX.jsonl"), ("pins", "LOG_PINS.tsv"),
                    ("removals", "LOG_REMOVALS.tsv")):
        if getattr(a, k) is None:
            setattr(a, k, home() / name)
    return {"add": cmd_add, "verify": cmd_verify, "pins": cmd_pins, "window": cmd_window,
            "retire": cmd_retire}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
