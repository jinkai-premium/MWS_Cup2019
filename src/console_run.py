# coding: utf-8
from typing import List
from pathlib import Path
from subprocess import check_output

import click

from src.models.Config import Config
from src.models.Types import EventLogs
from src.models.PlantUml import PlantUml
from src.models.ElasticSearchController import ElasticSearchController
from src.models.EventLog import EventLog_Logon, EventLog_Logoff, EventLog_DetectMalware


def main():
    """
    console:
        ```
        $ mwscup2019_jinkai-premium
        ```

    options:
        ```
        --input: input directory
            Note: Bulk Indice to ElasticSearch
            ex: --input="/path/to/your/directory"
                -> first, bulk indice your evtx files to elasticsearch

        --output: output filename
            ex: --output="out"
                -> generate [./out.uml, ./out.png]

        --nopng: generate only .uml file
            ex: --no-png="False"
                -> generate [./out.uml]

        ```
    """
    command()


@click.command()
@click.option('--input', help='Input Directory(include evtx files)')
@click.option('--output', help='Output filename')
@click.option('--nopng', default=False, help='')
def command(input, output, nopng):
    config = Config()

    if input is not None:
        script = config.root_directory / Path('scripts/indices_evtxfiles.py')
        check_output(f"python {script} {input}", shell=True)

    es = ElasticSearchController('_all')

    logs: List[EventLogs] = []
    detect_malware = [EventLog_DetectMalware(log) for log in es.search_by_eventids(eventids=[1116, 1117])]
    logon = [EventLog_Logon(log) for log in es.search_and_filter(filters=[
        {"terms": {"body.Event.System.EventID.#text": [4624]}},
        {"term": {"body.Event.EventData.Data.LogonType": 10}}
    ])]
    logoff = [EventLog_Logoff(log, logon) for log in es.search_and_filter(filters=[
        {"terms": {"body.Event.System.EventID.#text": [4634]}},
        {"term": {"body.Event.EventData.Data.LogonType": 10}}
    ])]

    logs.extend(logon)
    logs.extend(logoff)
    logs.extend(detect_malware)

    filename = output if output is not None else f"{config.DEFAULT_OUTPUT_DIR}/output"

    nopng = False if nopng is None else True
    PlantUml(Path(filename)).write_file(logs, nopng)
