import sqlite3, sys
c = sqlite3.connect("file:" + sys.argv[1] + "?mode=ro&immutable=1", uri=True)
for (s,) in c.execute("select sql from sqlite_master where name in ('kind_dk','kind_off','meta')"):
    print(s)
print(c.execute("select * from kind_dk limit 3").fetchall())
