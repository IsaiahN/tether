"""Read census run 1's census.tsv and malloc stats into the P1/P2 readings (the reviewer 2026-10-19 03:00 A3). READ ONLY.
argv: run_dir"""
import re
import sys

D = sys.argv[1]
pts, roots = {}, {}
with open(f"{D}/census.tsv", encoding="utf-8") as fh:
    for ln in fh:
        f = ln.rstrip("\n").split("\t")
        if f[0] == "POINT" and f[1] != "label":
            pts[f[1]] = f
        elif f[0] == "ROOT" and f[1] != "label":
            roots.setdefault(f[1], {})[f[2]] = f


def ms(label):
    t = open(f"{D}/mallocstats_{label}.txt", encoding="utf-8", errors="replace").read()

    def n(rx):
        m = re.search(rx, t)
        return int(m.group(1).replace(",", "")) if m else 0
    return {"arena_bytes": n(r"arenas \* \d+ bytes/arena\s*=\s*([\d,]+)"),
            "alloc": n(r"# bytes in allocated blocks\s*=\s*([\d,]+)"),
            "avail": n(r"# bytes in available blocks\s*=\s*([\d,]+)"),
            "unused_pools": n(r"unused pools \* \d+ bytes\s*=\s*([\d,]+)")}


G = 2**30
labels = ["after_load", "after_step1", "after_step2", "switch"]
print("label\tcommit_before_GiB\tcensus_s\tarena_GiB\talloc_GiB\tavail_GiB\tunused_pools_GiB\tsum_root_est_GiB\t"
      "lower_bound_roots\troots")
S = {}
for lab in labels:
    p, m, r = pts[lab], ms(lab), roots[lab]
    s = sum(int(x[12]) for x in r.values())
    S[lab] = (int(p[2]), m, s)
    print(f"{lab}\t{int(p[2]) / G:.3f}\t{p[4]}\t{m['arena_bytes'] / G:.3f}\t{m['alloc'] / G:.3f}\t{m['avail'] / G:.3f}\t"
          f"{m['unused_pools'] / G:.3f}\t{s / G:.3f}\t{sum(1 for x in r.values() if x[13])}\t{len(r)}")
c0, m0, s0 = S["after_load"]
c1, m1, s1 = S["switch"]
dc, L = c1 - c0, s1 - s0
print(f"\nDelta(commit) after_load->switch {dc} B = {dc / G:.3f} GiB")
print(f"Delta(arena bytes) {(m1['arena_bytes'] - m0['arena_bytes']) / G:.3f} GiB; Delta(alloc blocks) "
      f"{(m1['alloc'] - m0['alloc']) / G:.3f}; Delta(avail blocks) {(m1['avail'] - m0['avail']) / G:.3f}; "
      f"Delta(unused pools) {(m1['unused_pools'] - m0['unused_pools']) / G:.3f}")
print(f"L = Delta(sum of sampled root estimates) = {L / G:.3f} GiB; U = Delta(commit) - L = {(dc - L) / G:.3f} GiB")
print("\nper root Delta(est) after_load->switch, top 15 by |Delta| (root, len before -> after, est GiB before -> after, "
      "delta GiB, lower bound at switch, already_seen at switch):")
ra, rb = roots["after_load"], roots["switch"]
rows = []
for k in set(ra) | set(rb):
    a, b = ra.get(k), rb.get(k)
    ea, eb = int(a[12]) if a else 0, int(b[12]) if b else 0
    rows.append((eb - ea, k, a[4] if a else "-", b[4] if b else "-", ea, eb, b[13] if b else "", b[14] if b else ""))
for d, k, la, lb, ea, eb, bound, seen in sorted(rows, key=lambda x: -abs(x[0]))[:15]:
    print(f"  {k}\t{la} -> {lb}\t{ea / G:.3f} -> {eb / G:.3f}\t{d / G:+.3f}\t{bound}\t{seen}")
print("\ntop 10 roots by est at after_load (root, len, est GiB, sampled mean B, median, max):")
for k, x in sorted(ra.items(), key=lambda kv: -int(kv[1][12]))[:10]:
    print(f"  {k}\t{x[4]}\t{int(x[12]) / G:.3f}\t{x[7]}\t{x[8]}\t{x[9]}")
