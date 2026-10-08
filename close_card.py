"""Close a scorecard by id -- the recovery path for an interrupted run.

The API has no list endpoint, so an id that was never written down is unreachable. This reads
`runs/online_card_id.txt` (or takes one on the command line) and closes it.
"""
import sys

import arc_online


def main() -> None:
    arc_online._load_env()
    card = sys.argv[1] if len(sys.argv) > 1 else None
    if card is None:
        try:
            with open(arc_online.CARD_FILE, encoding="utf-8") as f:
                card = f.read().strip()
        except FileNotFoundError:
            sys.exit(f"no card id given and {arc_online.CARD_FILE} does not exist")
    import os

    from arc_agi import Arcade, OperationMode
    arc = Arcade(operation_mode=OperationMode.ONLINE,
                 arc_api_key=os.getenv("ARC_API_KEY", ""))
    closed = arc.close_scorecard(card)
    print(f"closed {card}: score={getattr(closed, 'score', None)}")
    for el in getattr(closed, "environments", []):
        for r in el.runs:
            print(f"  {r.guid}: levels_completed={r.levels_completed} "
                  f"score={r.score} actions={r.actions}")


if __name__ == "__main__":
    main()
