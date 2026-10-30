"""One-off edit for (4b): replace seven `return None` lines in interface._choose by line number,
asserting each is exactly `<indent>return None`, keeping each line's own ending."""
import sys

sys.dont_write_bytecode = True
path = sys.argv[1]
REPL = {
    671: ['return self._none(BLOCKED, "nothing offered", asker)'],
    690: ['return self._none(NO_WAY, "no reading of the subject in this state", asker)'],
    755: ['return self._none(self._tried(offered, intent.subject),',
          '                  "no cell lands the subject on the value (BECOME)", asker)'],
    850: ['return self._none(self._tried(offered, intent.subject),',
          '                  "no cell moves the subject that way (BECOME, signed)", asker)'],
    908: ['return self._none(self._tried(offered, intent.object or intent.subject),',
          '                  "no route to contact (TOUCH)", asker)'],
    912: ['return self._none(NO_WAY, "no table entry for this intent kind", asker)'],
    921: ['return self._none(NO_WAY, "no member separates anything here (DISTINGUISH)",',
          '                  asker)'],
}
raw = open(path, "rb").read().decode("utf-8")
lines = raw.splitlines(keepends=True)
for n, new in sorted(REPL.items(), reverse=True):
    ln = lines[n - 1]
    body = ln.rstrip("\r\n")
    end = ln[len(body):]
    assert body.strip() == "return None", (n, body)
    ind = body[:len(body) - len(body.lstrip())]
    lines[n - 1:n] = [ind + s + end for s in new]
open(path, "wb").write("".join(lines).encode("utf-8"))
print("replaced", len(REPL))
