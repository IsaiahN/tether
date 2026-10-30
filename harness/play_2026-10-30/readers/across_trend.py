"""Trend lines over the across-round table (read-only): thirds means and Spearman against round number."""
import csv, sys
sys.dont_write_bytecode = True
rows = list(csv.DictReader(open("across_table.tsv", encoding="utf-8"), delimiter="\t"))
def ranks(xs):
    o = sorted(range(len(xs)), key=lambda i: xs[i]); r = [0.0]*len(xs); i = 0
    while i < len(o):
        j = i
        while j+1 < len(o) and xs[o[j+1]] == xs[o[i]]: j += 1
        for k in range(i, j+1): r[o[k]] = (i+j)/2+1
        i = j+1
    return r
def sp(x, y):
    rx, ry = ranks(x), ranks(y); n = len(x); mx, my = sum(rx)/n, sum(ry)/n
    c = sum((a-mx)*(b-my) for a, b in zip(rx, ry)); vx = sum((a-mx)**2 for a in rx)**.5; vy = sum((b-my)**2 for b in ry)**.5
    return c/(vx*vy) if vx and vy else float("nan")
n = [int(r["n"]) for r in rows]
def col(k, f=float): return [f(r[k]) for r in rows]
bp = [float(r["bp35"].split("@")[0]) for r in rows]
series = {"steps/min": col("spm"), "steps": col("steps"), "wall": col("wall"), "settle": col("settle"), "reuse": col("reuse"),
          "mints": col("mints"), "names": col("names"), "lineage_MB": [x/1e6 for x in col("lbytes")], "bp35_first": bp,
          "owed_max": [float(r["owed"].split("(")[0]) for r in rows], "mint_deferred": col("md")}
for k, v in series.items():
    t = len(v)//3
    print(f"{k:14s} thirds {sum(v[:t])/t:9.2f} {sum(v[t:2*t])/t:9.2f} {sum(v[2*t:])/(len(v)-2*t):9.2f} | Spearman vs round {sp(n, v):+.2f} | min {min(v):.2f} max {max(v):.2f}")
nm = col("names"); lb = col("lbytes")
print("names per round:", sorted(set(int(nm[i+1]-nm[i]) for i in range(len(nm)-1))), "| bytes per round MB: min %.2f max %.2f" % (min((lb[i+1]-lb[i])/1e6 for i in range(len(lb)-1)), max((lb[i+1]-lb[i])/1e6 for i in range(len(lb)-1))))
miss = [(r["n"], r["missed"]) for r in rows if r["missed"] != "-"]
print("missed switches:", len(miss), "of", 24*len(rows), miss)
print("owed max with game:", [(r["n"], r["owed"]) for r in rows if float(r["owed"].split("(")[0]) >= 60])
