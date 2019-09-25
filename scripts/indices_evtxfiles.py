# coding: utf-8
import sys
from pathlib import Path

from pprint import pprint
from evtxtoelk import EvtxToElk


def main():
    """
    Overview:
        import evtx to elastic_search

    Usage:
        ```
        $ python indices_evtxfiles.py {TARGET_DIRECTORY}
        ```

    Requirements:
        elasticsearch & kibana, or run `hit-parser/scripts/docker_elk.sh`
    """
    evtx_files = Path(sys.argv[1]).glob('**/*.evtx')
    for evtx in evtx_files:
        print(f"index: {evtx}")
        print(f"index-name: {evtx.parent.stem}")
        EvtxToElk.evtx_to_elk(evtx, 'http://localhost:9200', elk_index=evtx.parent.stem, bulk_queue_len_threshold=3000)
        print()


if __name__ == '__main__':
    main()
