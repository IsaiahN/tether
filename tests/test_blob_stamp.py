"""C-IE-1, (i-e) EOL-independent stamps (the reviewer 2026-10-14 10:19; 2026-10-15 18:42).

  MF       the same file written LF and CRLF gives ONE files_blob; one changed byte gives two
  control  files_sha (the old stamp) differs for that LF/CRLF pair, so the pair can tell them apart
  witness  blob_id of a tracked file equals `git hash-object` of its LF form
  library  library_blob over a temp LIBRARY_FILES layout behaves the same
  header   Attribution.code() carries files_blob and library_blob with the arm ON, neither OFF
  order    two processes importing different module sets give one files_blob (the disk set)
  disk     a .py under an excluded directory name is skipped; one under a plain directory kept

    python tests/test_blob_stamp.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile

import _repo  # noqa: F401  the repo root on sys.path (tests/, 4d)

sys.dont_write_bytecode = True

from instruments import Attribution  # noqa: E402

BODY = b"def f():\n    return 1\n\nx = f()\n"


def _one(root: str, data: bytes, name: str = "a.py") -> str:
    p = os.path.join(root, name)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "wb") as fh:
        fh.write(data)
    return p


def main() -> None:
    crlf = BODY.replace(b"\n", b"\r\n")
    with tempfile.TemporaryDirectory() as lf_d, tempfile.TemporaryDirectory() as cr_d, \
            tempfile.TemporaryDirectory() as ch_d:
        lf, cr = _one(lf_d, BODY), _one(cr_d, crlf)
        ch = _one(ch_d, BODY.replace(b"1", b"2"))
        assert Attribution.files_sha([lf], lf_d) != Attribution.files_sha([cr], cr_d), (
            "control: the old stamp does not see the LF/CRLF pair, so the MF proves nothing")
        assert Attribution.blob_sha([lf], lf_d) == Attribution.blob_sha([cr], cr_d), (
            "MF: LF and CRLF give two files_blob")
        assert Attribution.blob_sha([lf], lf_d) != Attribution.blob_sha([ch], ch_d), (
            "MF: one changed byte gives one files_blob")
        print("  MF LF and CRLF give one files_blob (files_sha gives two); one changed byte, two")
        for d, data in ((lf_d, BODY), (cr_d, crlf)):
            for p in Attribution.LIBRARY_FILES[:3]:
                _one(d, data, p)
        assert Attribution.library_files(lf_d) and Attribution.blob_sha(
            Attribution.library_files(lf_d), lf_d) == Attribution.blob_sha(
            Attribution.library_files(cr_d), cr_d), "library: LF and CRLF give two library_blob"
        print(f"  library {len(Attribution.library_files(lf_d))} files: one library_blob for LF"
              " and CRLF")
    here = _repo.ROOT
    with open(os.path.join(here, "armflag.py"), "rb") as fh:
        data = fh.read()
    git = subprocess.run(["git", "hash-object", "--stdin", "--no-filters"], cwd=here,
                         input=data.replace(b"\r\n", b"\n"), capture_output=True, check=True)
    assert Attribution.blob_id(data) == git.stdout.decode().strip(), "witness: not git's blob id"
    print(f"  witness blob_id(armflag.py) == git hash-object: {git.stdout.decode().strip()[:12]}")
    code = [sys.executable, "-B", "-c",
            "import json, instruments; c = instruments.Attribution.code(); "
            "print(json.dumps([k in c for k in ('files_blob', 'library_blob')]))"]
    env = {k: v for k, v in os.environ.items() if not k.startswith("TETHER_")}
    on = subprocess.run(code, cwd=here, env=env, capture_output=True, text=True, check=True)
    off = subprocess.run(code, cwd=here, env=env | {"TETHER_BLOB_STAMP": "0"},
                         capture_output=True, text=True, check=True)
    assert json.loads(on.stdout.splitlines()[-1]) == [True, True], on.stdout
    assert json.loads(off.stdout.splitlines()[-1]) == [False, False], off.stdout
    print("  header ON carries files_blob and library_blob; OFF carries neither")
    order = ("import json, {first}instruments; c = instruments.Attribution.code(); "
             "print(json.dumps([c['files_blob'], c['n_files']]))")
    a = subprocess.run([sys.executable, "-B", "-c", order.format(first="")], cwd=here, env=env,
                       capture_output=True, text=True, check=True)
    b = subprocess.run([sys.executable, "-B", "-c", order.format(first="tether, gridworld, ")],
                       cwd=here, env=env, capture_output=True, text=True, check=True)
    (blob_a, n_a), (blob_b, n_b) = (json.loads(x.stdout.splitlines()[-1]) for x in (a, b))
    assert n_a != n_b, ("order: both orders imported the same files, so it proves nothing", n_a)
    assert blob_a == blob_b, "order: two import orders give two files_blob"
    print(f"  order {n_a} vs {n_b} files imported: one files_blob")
    with tempfile.TemporaryDirectory() as d:
        keep = _one(d, BODY, "pkg/m.py")
        for x in Attribution.BLOB_EXCLUDE:
            _one(d, BODY, f"{x}/skip.py")
        got = [os.path.normpath(x) for x in Attribution.disk_files(d)]
        assert got == [os.path.normpath(keep)], got
    print(f"  disk set: a .py under each of {len(Attribution.BLOB_EXCLUDE)} excluded names is"
          " skipped, one under a plain directory kept")
    print("blob stamp: OK")


if __name__ == "__main__":
    main()
