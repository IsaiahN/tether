"""The repo root on sys.path for a test run from tests/ (4d; the reviewer 2026-10-22 04:03, 07:40).
Every test imports this first. ROOT is the repo root: the agent's modules, harness/, conform/ and
environment_files/ live there."""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
