# tests

One file per feature, each with its must-fail checks (a check that has to go red when the feature is removed). `known_red.py` lists the reds known before a change. Every test here runs in under ten minutes; game-length runs are not tests in this folder. Run one with `python tests/<name>.py`.
