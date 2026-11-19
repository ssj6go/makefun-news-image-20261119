"""A working news-image-daily entry (Python 3.13, standard library only).

The image is the entry.png beside this file, and the program copies it
to /output/entry.png. The gate takes a whole PNG or JPEG of at most
1 MiB and 1024 by 1024 pixels, and the judge sees exactly the bytes copied,
so the copy is written to a temporary file first, checked to be a whole
PNG within the size cap, and only then moved into place: a failed run
never leaves a partial entry.png behind.

Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
  mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil

MAX_BYTES = 1048576
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
PNG_IEND = b"IEND"

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
DST = os.path.join(OUT_DIR, "entry.png")
TMP = DST + ".tmp"

os.makedirs(OUT_DIR, exist_ok=True)
shutil.copyfile(SRC, TMP)

with open(TMP, "rb") as f:
    data = f.read()

if data[:8] != PNG_MAGIC:
    os.remove(TMP)
    raise SystemExit("entry.png is not a PNG (bad magic bytes)")
if PNG_IEND not in data[-12:]:
    os.remove(TMP)
    raise SystemExit("entry.png is not a whole PNG (no IEND trailer)")
if len(data) > MAX_BYTES:
    os.remove(TMP)
    raise SystemExit(f"entry.png is {len(data)} bytes, over the 1 MiB cap")

os.replace(TMP, DST)
