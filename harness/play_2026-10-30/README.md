# harness/play_2026-10-30: the seat's harness, reader and edit-tool scripts

The reviewer's r447 (Isaiah, 2026-10-30 14:22 CDT) asked for all uncommitted work to be uploaded and reviewed once as one package. This folder holds every script the seat ran from outside the repository. They come from two places:

- the session scratchpad;
- the PLAY run directories under `C:/TETHER_RUNS/S6_2026-10-19/`.

**Byte-for-byte.** Every file is stored exactly as it is on the box. `.gitattributes` marks the folder `-text`, so git does not convert line endings. `ruff.toml` turns lint off here, because these are records, not code to fix.

**Manifest.** `MANIFEST.tsv` gives, for each file:

- its class;
- its path here;
- its source path on the box;
- its sha256, re-hashed after the copy;
- its size in bytes.

**Excluded, and not here:**

- the lineage (`memory.db` and the generations);
- run streams (`stream.jsonl`) and ledgers;
- `chain.log`, `switch.tsv`, `mem.tsv` and every other run log;
- every backup;
- the five whole-file copies of `tether.py` in the scratchpad: `t_orig.py`, `tether_act_full.py`, `tether_affb69d.py`, `tether_arm12.py`, `tether_b17.py`. These are AGENT probe or backup snapshots.
  - `tether_arm12.py` is af6f0cd's `tether.py` with arm 2 dropped from one condition (3 lines).
  - The other four were not diffed against commits.
- `e4_stream_eadee1a.py`, a copy of the repository's own `harness/mem_store/e4_stream.py` at eadee1a;
- the seven scratch test drafts. They are AGENT-side and sit on their own branch, `wip/scratch-test-drafts-2026-10-30`.

A secret scan found no key, token, credential or email in any file. The patterns were:

> secret, token, api key, password, bearer, gateway, credential, arcprize, authorization, sk-ant, memory.db, sqlite, TETHER_RUNS, lineage/, plus key-shaped strings and emails

## Classes

| class | folder | what it is | how the class was set |
|---|---|---|---|
| HARNESS-PLAY | `play/` | the files PLAY24 runs that are not in the tree: `play/E4B_SPY`, `play/PF/pf_check.py`, `play/PLAY24` | checked against PLAY24's `play_chain.want` and its `SPY` pin |
| HARNESS | `scripts/` | launchers, carriers, backups and test runners: `auto_play*.ps1`, `want*.sh`, `make_play*.py`, `carry24.py`, `backup_lineage.py`, `run_*.sh`, `*_run.sh` and similar | by file name |
| READER | `readers/` | read-only reads of run outputs, probes and scans | by file name: whatever is not HARNESS or EDIT-TOOL |
| EDIT-TOOL | `edits/` | scripts that wrote an edit into a repository file, a doc or a ledger | by file name. Whether each edit landed in a commit was not checked file by file |

## The PLAY set

| file | sha256[:16] | used by |
|---|---|---|
| `E4B_SPY/e4b_box.py` | de890479b92db1ea | PLAY20-PLAY24 (`play_chain.want` field 1) |
| `E4B_SPY/e4b_box.credit_on.20261029T213714Z.py` | de890479b92db1ea | dated copy, identical to `e4b_box.py` |
| `E4B_SPY/e4b_box.credit_off.20261030T043350Z.py` | 3aecb6cebedd7df1 | PLAY19 (credit OFF from round 3; the reviewer r344), kept as a dated copy |
| `E4B_SPY/e4b_run.py` | ab811e2660cbbba7 | PLAY19-PLAY24 |
| `E4B_SPY/e4b_read.py` | 33b4253fb443063e | PLAY19-PLAY24 |
| `E4B_SPY/break_audit.py` | ef8f4ca65e024d5a | PLAY19-PLAY24 |
| `E4B_SPY/kind_spy.py` | 0df3871e1b49935b | PLAY24 (`SPY` pin). `realise` passes `split` through (the reviewer r440, r441) |
| `E4B_SPY/kind_spy.py.0622d0e9` | 0622d0e95995f3b4 | PLAY19-PLAY23. Its `realise` wrapper lacked `split`, which caused PLAY23's c146 agent_fault |
| `PF/pf_check.py` | 9d578a9152bacbdd | PLAY19-PLAY24 (`CHK`) |
| `PLAY24/play_chain.sh` | f2dfb6fc6d6f44f6 | PLAY24's chain. The launched copy is `play_chain.launched.<utc>.sh` in the run directory |
| `PLAY24/precheck.sh` | d88a2b1c886d8f9f | PLAY24's precheck |
| `PLAY24/play_across.py` | fc80c1f78544dfbb | PLAY19-PLAY24 |
| `PLAY24/spy_sweep.py` | 70ede177da985471 | PLAY24 precheck: red if any kind_spy wrapper's signature is behind its original (the reviewer r441) |
| `PLAY24/play_chain.want` | 00a41055f76675ca | PLAY24's sha pins for the files above and the tree's own files |

## PLAY24's pins

- Trees:
  - general-agent: `G=eadee1aa0c5c6f7e24381099d8573f28be254e04`
  - arc-solver-agent: `H=26a68e0e23bef27a622ccfa5f86bb01d83f04126` (eadee1a + README)
- `SPY=0df3871e1b49935b`, the kind_spy.py file.
- spy_sweep: 70ede177da985471.
- The lineage is read from `C:/TETHER_RUNS/E4_2026-10-18/lineage` and is never copied here.
