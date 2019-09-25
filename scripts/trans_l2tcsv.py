# coding: utf-8
import sys
import subprocess
from pathlib import Path

"""
Overview:
    trans evtx -> l2tcsv.

Usage:
    ```
    $ python trans_l2tcsv.py {TARGET_DIRECTORY}
    ```
"""

basedir = Path(sys.argv[1])
sourcefiles = list(basedir.glob('**/*.evtx'))

for evtx in sourcefiles:
    subprocess.run(f"docker run -v {evtx.parent.resolve()}:/data log2timeline/plaso log2timeline /data/{evtx.stem}.l2t /data/{evtx.stem}.evtx", shell=True)
    subprocess.run(f"docker run -v {evtx.parent.resolve()}:/data log2timeline/plaso psort -o l2tcsv -w /data/{evtx.stem}.csv /data/{evtx.stem}.l2t", shell=True)
