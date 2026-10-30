import sys
p = sys.argv[1]
raw = open(p, "rb").read().decode("utf-8")
nl = "\r\n" if "\r\n" in raw else "\n"
lines = raw.split(nl)
ON = ("**ON (code), superseded: default ON since Isaiah 2026-10-15 07:53, 17:26 (annotated 2026-10-20, "
      "the reviewer 14:27)**; was: OFF pending reading")
SUB = ("**still OFF (default False), inert: read only by _target_lookup, which runs only while "
       "TETHER_WANT_TARGET is OFF (annotated 2026-10-20, the reviewer 14:27)**; was: OFF pending reading")
done = 0
for i in range(478, 484):
    assert "OFF pending reading" in lines[i] and "superseded" not in lines[i], (i + 1, lines[i][:80])
    lines[i] = lines[i].replace("OFF pending reading", SUB if "WANT_TARGET_SUBJECT" in lines[i] else ON, 1)
    done += 1
open(p, "wb").write(nl.join(lines).encode("utf-8"))
print("annotated", done, "rows; newline", repr(nl))
