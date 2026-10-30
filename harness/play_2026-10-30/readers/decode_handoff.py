"""Decode the Drive download (JSON, base64 content) to UTF-8 text. argv: json_file out_txt"""
import base64
import json
import sys

d = json.load(open(sys.argv[1], encoding="utf-8"))
raw = base64.b64decode(d["content"])
open(sys.argv[2], "wb").write(raw)
print(d.get("title"), len(raw))
