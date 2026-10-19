# E5.1: the E4 harness

One agent. Games 00-17 ran on 38b2daa, games 18-24 and the probe on 7c77689. The only agent change between them is a crash guard (ALPHA-LAST), which alters nothing except where the older tree crashed. The harness cap counted load time on 38b2daa and play time only on 7c77689, so games 00-17 had up to ~85 s less play.

This folder holds the drivers, launchers and read-only readers behind every posted E4 reading. No agent code. The run data and the local package stay in C:\TETHER_RUNS\E4_2026-10-18 (E51_package/INDEX.tsv).

- e4_stream.py (sha256[:16] 3b091fbddae9cfe7): the stream driver as census run 1 ran it (adds --slice-steps and --census).
- e4_stream.probe_cf5a455.py (sha256[:16] cf5a4553acbdee23): byte-identical to the file the E4b 5-game probe ran.
- census_heap.py, run_census.py, census_watch.sh, census_read.py, compare_rows.py, census_selftest.py: census run 1 (sc25, 3 steps, on a lineage copy) and its readings.
