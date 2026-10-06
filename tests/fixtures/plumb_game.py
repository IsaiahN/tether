"""A SYNTHETIC ENGINE GAME FOR PLUMBING ONLY -- no ARC content. One block, four moves, and the game
ends (GAME_OVER) after a fixed number of moves, so a run through the real server is short.
Reachable only from test_entry's multi-process scorecard check, which copies it into throwaway
game directories; the bundle never ships it. What it proves is WIRING, never capability."""
from arcengine import ARCBaseGame, GameAction, Level, Sprite

MOVES = {GameAction.ACTION1: (0, -1), GameAction.ACTION2: (0, 1),
         GameAction.ACTION3: (-1, 0), GameAction.ACTION4: (1, 0)}
# anchor: a loop bound for a plumbing fixture, not a game parameter.
LIFE = 8


class Plumb(ARCBaseGame):
    def __init__(self, seed: int = 0) -> None:
        level = Level(sprites=[Sprite([[3, 3], [3, 3]], name="block", x=30, y=30)],
                      grid_size=(64, 64))
        super().__init__(game_id="plumb", levels=[level], available_actions=[1, 2, 3, 4],
                         seed=seed)
        self.moves = 0

    def step(self) -> None:
        if self.action.id in MOVES:
            self.try_move("block", *MOVES[self.action.id])
            self.moves += 1
            if self.moves >= LIFE:
                self.lose()
        self.complete_action()
