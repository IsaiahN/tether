# scratch_test_drafts: seven AGENT-side test drafts from the seat's scratchpad (r447)

These are the test files the seat kept in its session scratchpad. They are AGENT-side, so per r447 they get their own branch, apart from the harness branch.

- They are stored byte-for-byte; see `MANIFEST.tsv` for sha256 and size.
- They did not run in PLAY24. No PLAY runs tests.
- Six of the seven match no commit, byte-for-byte or with LF line endings.
- `test_window.full.py` matches 29b85fe (2026-10-26) exactly.
- The other six are drafts or stubs of tests whose final forms may be in `tests/`. That was not checked file by file.
- None is wired into `tests/`. This folder is outside the test tree and lint is off here.
