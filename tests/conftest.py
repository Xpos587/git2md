"""Makes the ``src`` layout importable so ``pytest`` works from the repo root."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
