# Running the agent on Kaggle

How to put the agent into the ARC Prize 2026 (ARC-AGI-3) competition, as it was done on 2026-11-13, when the first commit run went end to end. It took four runs to get there. Each of the first three hit something about how Kaggle stores uploads that you can't see from the code, so that is written down here.

## What goes up

Two datasets and one notebook. The notebook is internet-off, so everything the agent needs comes from these.

| Upload | What it holds | Built by |
|---|---|---|
| **Code dataset** | the repo at one commit (agent code, `library/`, `requirements.lock`), plus a marker file and a manifest of every file's sha256 | `kaggle/build_dataset.py` |
| **Lineage dataset** (the memory) | one frozen copy of a lineage folder: the generations (`gen_*.json`, `ak_*.json`), `memory.db` and its `-shm`/`-wal` files, plus a marker and a manifest | `kaggle/build_lineage.py` |
| **Notebook** | `kaggle/tether_b.ipynb` (shape B: parallel workers). Generated from `kaggle/make_notebook.py`; never edit the `.ipynb` by hand | `python kaggle/make_notebook.py` |

The competition's own data (attached automatically) supplies the `arc_agi` and `arcengine` wheels, installed offline.

## The release that ran (2026-11-13)

| | |
|---|---|
| Code commit | arc-solver-agent `5f811fa6da5d16ca02fc43bb7c3bcad198582d09` (tree `10373c30`) |
| Code dataset | 714 files, manifest sha256 `1bbda72f47b82fe28fc7e87a8d1979744af805febfe44e61fe1931db10ac5385` |
| Lineage dataset | head `edfe475c7e5ff724`, 950 files, 1,862,848,884 bytes, manifest sha256 `ff50b9bcd2f382d6e8b2850a2a75b12a0c7c72ee6772f1b8da5083b761a8ee2e` |
| Notebook | `tether_b.ipynb` from development `e03f19b` (sha256 `a3dfe757...`) |

The tag `kaggle-2026-11-13` marks the code commit.

## Steps

1. **Build the code dataset** from a checkout with `core.autocrlf=false` (a Windows checkout with CRLF line endings gives a different manifest):
   ```
   python kaggle/build_dataset.py <commit> <OUT_DIR>
   ```
   Read `OUT_DIR/scan.txt` before uploading: it prints every line that looks like it assigns a key, secret or password. Today it has 4 known, harmless lines (test keys and a design note).
2. **Build the lineage dataset** from a lineage folder no run is writing to, naming the head you expect:
   ```
   python kaggle/build_lineage.py <LINEAGE_DIR> <EXPECTED_HEAD> <OUT_DIR>
   ```
   It refuses if the copy's head differs or the source changed during the copy. Its `scan.txt` should be empty.
3. **Smoke it locally** before uploading. `run_local.py` runs every notebook cell against a local gateway, the way Kaggle would:
   ```
   python kaggle/run_local.py kaggle/tether_b.ipynb <CODE_OUT_DIR> <WORK_DIR> <ENV_DIR> <PORT> --lineage-ds <LINEAGE_OUT_DIR> --n-games 1
   ```
   Use absolute paths. Check: every cell OK, "every sha256 equals the manifest", the lineage head line, faults 0.
4. **Zip and upload.** Zip each dataset's payload folder (`code/` or `lineage/`) and upload the zip with the marker file, `MANIFEST.sha256` and `scan.txt` beside it. For a new version of an existing dataset, delete the old files first.
5. **Import the notebook**, attach both datasets and the competition data, and run the commit.

## The three upload quirks, and how each is handled

**1. A zip of a folder lands nested one level.** Kaggle unpacks an uploaded `code.zip` into a `code/` folder. If the zip itself contains a `code/` folder, the files end up at `code/code/`. The notebook's check then found the first manifest file missing (runs 1 and 2: `.gitattributes`, then `CHANGELOG.md`).
*Handled in the notebook:* `_place()` sees a folder whose only entry has the same name, copies from inside it, and prints "nested one level". Both datasets go through it.

**2. Kaggle unpacks archive-type files inside an upload.** `tests/data/cue_key_path/dc22_c24.json.gz` arrived decompressed, so its manifest path was missing (run 3).
*Handled in the build:* `build_dataset.py` leaves out files ending `.gz .zip .tar .tgz .bz2 .xz .7z .rar`, lists them in the marker's `"dropped"` field, and never puts them in the manifest. At 5f811fa that's two test-data files the agent never reads. The lineage holds no archive-type files.

**3. Dot-named files.** `.gitattributes` and `.gitignore` are also left out and listed in `"dropped"`. This was first blamed for run 1's failure; the real cause was the nesting in quirk 1. Leaving them out is harmless (the agent reads neither), so it stays.

**And one guard:** the notebook now lists every missing manifest file in one pass, with what its folder holds, before stopping. Before, it stopped at the first missing file, which is why each run found only one problem. If Kaggle drops an empty file (the lineage's `memory.db-wal` is 0 bytes), the notebook re-creates it; the sha256 check still judges it.

## What a good run looks like

```
code folder holds 1 entries, first ['code']
code stored as folder, nested one level
copied 714 files to /kaggle/working/tether; every sha256 equals the manifest
agent imports ok
lineage folder holds 1 entries, first ['lineage']
lineage stored as folder, nested one level
lineage copied and checked in ... s: 950 names, head edfe475c7e5ff724
```
Then the games run. In a submission run (the private set) no errors come back, only a score, so a clean commit run is the last place to catch a problem.

## Rules

- The uploads are Isaiah's. Builds and smokes are done by the seats; nothing here uploads anything.
- general-agent carries no Kaggle material; this page lives on development and arc-solver-agent only.
- Earlier uploads and what a later run must know before using them: `UPLOADS.md`.
