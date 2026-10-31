"""A LOCAL STAND-IN FOR THE COMPETITION GATEWAY, for running the notebook here before any upload: the arc_agi package's
own server (Arcade.listen_and_serve) in competition mode, over the local environment_files, offline. When a scorecard
closes, what the server reports is written to OUT/scorecard_<card>.json -- what the competition's gateway scores.
    python kaggle/local_gateway.py ENV_DIR OUT PORT"""
import json
import os
import sys

sys.dont_write_bytecode = True
ENV_DIR, OUT, PORT = sys.argv[1], sys.argv[2], int(sys.argv[3])
os.makedirs(OUT, exist_ok=True)

from arc_agi import Arcade, OperationMode  # noqa: E402


def closed(sc) -> None:
    dump = sc.model_dump(mode="json") if hasattr(sc, "model_dump") else repr(sc)
    with open(os.path.join(OUT, f"scorecard_{sc.card_id}.json"), "w", encoding="utf-8") as fh:
        json.dump(dump, fh, indent=1, default=repr)


Arcade(operation_mode=OperationMode.OFFLINE, environments_dir=ENV_DIR).listen_and_serve(
    host="127.0.0.1", port=PORT, competition_mode=True, on_scorecard_close=closed)
