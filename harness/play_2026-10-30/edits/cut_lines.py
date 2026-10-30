"""Remove lines [a, b) (1-based) from a file, asserting the first removed line's text first.
argv: path, a, b, expected first line prefix. Keeps the file's own line endings."""
import sys

sys.dont_write_bytecode = True
path, a, b, want = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
lines = open(path, encoding="utf-8", newline="").read().splitlines(keepends=True)
assert lines[a - 1].startswith(want), (lines[a - 1], want)
del lines[a - 1:b - 1]
open(path, "w", encoding="utf-8", newline="").write("".join(lines))
print("removed", b - a, "lines")
