# 13.3 game-type census

13.3 GAME-TYPE CENSUS -- A READING, NEVER AN INPUT. The agent never loads this file; no agent code imports or reads docs/census (checked in the smoke). Records only: the 13.1 calibration rows at d662c2d (OFF rows: CALC, the 21:10 master; ON rows: CALD, the 17:46 master, else CALC's ON lanes; a lane cut before its row is censored), each game's metadata.json, and its code for a named limit. A cell no record fills reads 'not in records'. Seat's reading, written blind (the reviewer seals its own, 2026-10-16 14:49). ALL WALLS ARE AT d662c2d (pre-repoint, pre-defaults-flip, before 7d/7h/7f/3a): they describe that commit, not today's head, and are not current cost.

| game | mode (metadata tags) | actions taken (OFF row) | move/action limit | wall OFF median/max s (cycles) | wall ON median/max s (cycles) | family |
|---|---|---|---|---|---|---|
| ar25 | both | ACTION1, ACTION2, ACTION3 | not in records; died at step 64 on 07-24 | 42.5 / 91.3 (3) | 213.2 / 523.7 (3) | not in this project's records |
| bp35 | both | ACTION3, ACTION4, ACTION6 | not in records; died at step 16 on 07-24 | 180.4 / 286.4 (3) | no row written: the lane was cut before its row; no cycle finished in the lane | not in this project's records |
| cd82 | both | ACTION1, ACTION2, ACTION3, ACTION4 | not in records (the game code is obfuscated; no named limit found) | 18.6 / 76.3 (4) | 281.2 / 575.4 (4) | not in this project's records |
| cn04 | both | ACTION1, ACTION2, ACTION3, ACTION4, ACTION5 | not in records; died at step 75 on 07-24 | 22.0 / 37.5 (5) | 202.6 / 266.9 (5) | not in this project's records |
| dc22 | both | ACTION1, ACTION2, ACTION3 | not in records (the game code is obfuscated; no named limit found) | 24.2 / 79.9 (3) | 833.7 / 1066.7 (3) | not in this project's records |
| ft09 | not in records ([]) | ACTION6, RESET | not in records (the game code is obfuscated; no named limit found) | 1.3 / 1.3 (5) | 60.8 / 2306.3 (5) | not in this project's records |
| g50t | avatar (keyboard) | ACTION1, ACTION2, ACTION3, ACTION4, ACTION5 | not in records (the game code is obfuscated; no named limit found) | 11.7 / 59.8 (5) | 177.0 / 503.2 (5) | not in this project's records |
| ka59 | both | ACTION1, ACTION2, ACTION3 | not in records (the game code is obfuscated; no named limit found) | 10.7 / 44.3 (3) | 162.2 / 499.8 (3) | not in this project's records |
| lf52 | click-only | ACTION1, ACTION2, ACTION3, ACTION4, ACTION6 | not in records; died at step 64 on 07-24 | 1.8 / 41.5 (5) | 2.8 / 2.8 (1) censored | not in this project's records |
| lp85 | click-only | ACTION6, RESET | not in records (the game code is obfuscated; no named limit found) | 0.8 / 0.9 (5) | 5.5 / 639.5 (5) | not in this project's records |
| ls20 | avatar (keyboard) | ACTION1, ACTION2, ACTION3 | not in records (the game code is obfuscated; no named limit found) | 24.3 / 54.5 (3) | 376.9 / 695.3 (3) | not in this project's records |
| m0r0 | both | ACTION1, ACTION2, ACTION3 | not in records (the game code is obfuscated; no named limit found) | 11.3 / 29.2 (3) | 90.8 / 187.2 (3) | not in this project's records |
| r11l | click-only | ACTION6, RESET | 60 actions (r11l.py 1407: _max_actions = 60; 1809 ends the level at it); died at step 60 on 07-24 | 7.2 / 21.8 (3) | 109.2 / 689.4 (3) | not in this project's records |
| re86 | both | ACTION1, ACTION2 | not in records (the game code is obfuscated; no named limit found) | 20.5 / 40.5 (2) | 238.1 / 475.3 (2) | not in this project's records |
| s5i5 | click-only | ACTION6, RESET | not in records; died at step 50 on 07-24 | 8.2 / 10.5 (3) | 154.8 / 591.5 (3) | not in this project's records |
| sb26 | both | ACTION5, ACTION6, ACTION7, RESET | 64 energy (sb26.py 723: an energy of 64; what spends it is not read here); died at step 65 on 07-24 | 1.7 / 8.6 (5) | 117.2 / 502.9 (5) | not in this project's records |
| sc25 | both | ACTION1, ACTION2, ACTION3 | not in records; died at step 52 on 07-24 | 28.1 / 35.8 (3) | 521.9 / 826.0 (3) | not in this project's records |
| sk48 | both | ACTION1, ACTION2, ACTION3 | not in records (the game code is obfuscated; no named limit found) | 214.1 / 254.5 (3) | no row written: the lane was cut before its row; no cycle finished in the lane | not in this project's records |
| sp80 | both | ACTION1, ACTION2, ACTION3, ACTION4, ACTION5 | not in records; died at step 30 on 07-24 | 12.7 / 17.7 (5) | 112.1 / 345.8 (5) | not in this project's records |
| su15 | click-only | ACTION6, ACTION7, RESET | not in records; died at step 43 on 07-24 | 0.5 / 0.6 (4) | 174.6 / 425.0 (4) | not in this project's records |
| tn36 | click-only | ACTION6, RESET | not in records; died at step 71 on 07-24 | 23.4 / 30.3 (3) | 4.6 / 4.6 (1) censored | not in this project's records |
| tr87 | avatar (keyboard) | ACTION1, ACTION2 | not in records (the game code is obfuscated; no named limit found) | 46.6 / 91.9 (2) | no row written: the lane was cut before its row; no cycle finished in the lane | not in this project's records |
| tu93 | both | ACTION1, ACTION2, ACTION3 | not in records; died at step 50 on 07-24 | 25.4 / 54.2 (3) | 2.0 / 2.0 (1) censored | not in this project's records |
| vc33 | click-only | ACTION6, RESET | not in records; died at step 50 on 07-24 | 3.8 / 4.8 (3) | 63.5 / 103.7 (3) | not in this project's records |
| wa30 | avatar (keyboard) | ACTION1, ACTION2, ACTION3 | not in records (the game code is obfuscated; no named limit found) | 5.9 / 10.5 (3) | 117.1 / 162.6 (3) | not in this project's records |

Counts by mode: avatar (keyboard) 4, both 13, click-only 7, not in records ([]) 1

## Another record: the 07-24 coverage census

COVERAGE_CENSUS.md (branch redux-triality, run_policy_live, 80 actions), relayed verbatim by the reviewer 2026-10-16 15:06. The family is THE ROUTER'S CHOICE ON 07-24, NOT A GAME FACT.

- directional: ar25 death@64 · bp35 death@16 · cd82 stall · cn04 death@75 · dc22 stall · ka59 stall · ls20 stall · re86 stall · sc25 death@52 · sk48 stall · sp80 death@30 · tu93 death@50 · wa30 stall.
- click: ft09 stall · lp85 stall · r11l death@60 · s5i5 death@50 · su15 death@43 · tn36 1 level, death@71 (L2) · vc33 death@50.
- effect: g50t stall · lf52 death@64 · sb26 death@65 · tr87 stall.
- two_body: m0r0 1 level, survives to cap.

Observed, two of two: the two games whose code names a limit died at it on 07-24 (r11l: limit 60, death@60; sb26: energy 64, death@65). This is not generalised to the other deaths (s5i5, vc33 and tu93 at 50; ar25 and lf52 at 64), whose limit cell reads 'not in records; died at step N on 07-24' (Fig 9: two coincidences do not prove a third).
Where the records disagree: ft09 has no tags and was routed click; lf52 is tagged click, took ACTION1-4 in its OFF row, and was routed effect.
