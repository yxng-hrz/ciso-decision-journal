"""Backward-compatible entry point (v1). Prefer: python tools/ciso.py board-pack"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ciso  # noqa: E402

if __name__ == "__main__":
    sys.exit(ciso.main(["board-pack", *sys.argv[1:]]))
