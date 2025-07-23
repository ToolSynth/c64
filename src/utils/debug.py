import pdb
import sys
from pathlib import Path


def custom_brk_point() -> None:
    sys.stdin = Path.open("/dev/stdin")
    pdb.set_trace()
