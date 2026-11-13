# conform

The agent's own checks, not its behaviour. `arms.py` is the register of every switch (`TETHER_*`) with why it exists and its default; `check.py` / `fast_check.py` are the commit gate ("the six" and the quick suite); `figtext.py` regenerates `docs/01-FOUNDATIONS/03-FIGURES_TEXT.md` from the SVGs in `figures/`; the rest are the wiring, lint and identity checks the gate runs. Nothing here runs during play.
