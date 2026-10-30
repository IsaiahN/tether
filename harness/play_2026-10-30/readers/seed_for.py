import os, random, sys
games = sorted(os.listdir(sys.argv[1]))
assert len(games) == 25, games
want = sys.argv[2]
for i in range(100000):
    s = f"{i:08x}"
    if random.Random(s).sample(games, len(games))[0] == want:
        print(s, random.Random(s).sample(games, len(games))[:3])
        break
