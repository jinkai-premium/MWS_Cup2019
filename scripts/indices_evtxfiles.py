# coding: utf-8
import sys
from pathlib import Path

from evtxtoelk import EvtxToElk

sys.path.append(str(Path(__file__).parent.parent))
from src.models.Config import Config


def main():
    """
    Overview:
        bulk_indice evtx to elastic_search

    Usage:
        ```
        $ python indices_evtxfiles.py {TARGET_DIRECTORY}
        ```

    Requirements:
        elasticsearch & kibana, or run `hit-parser/scripts/docker_elk.sh`
    """
    configs = Config()
    es_url = f"{configs.ELASTICSEARCH_HOST}:{configs.ELASTICSEARCH_PORT}"

    evtx_files = Path(sys.argv[1]).glob('**/*.evtx')
    for evtx in evtx_files:
        print(f"index: {evtx}")
        print(f"index-name: {evtx.parent.stem}")
        EvtxToElk.evtx_to_elk(evtx, es_url, elk_index=evtx.parent.stem, bulk_queue_len_threshold=3000)
        print()


if __name__ == '__main__':
    main()
