# coding: utf-8
from typing import List
from pathlib import Path

from src.models.Config import Config
from src.models.Types import EventLogs
from src.models.PlantUml import PlantUml
from src.models.ElasticSearchController import ElasticSearchController
from src.models.EventLog import EventLog_Logon, EventLog_Logoff, EventLog_DetectMalware


def main():
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

    # failed_logon = es.search_by_eventids(eventids=[4634])

    logs.extend(logon)
    logs.extend(logoff)
    logs.extend(detect_malware)

    config = Config()

    filename = input(f"Enter Output FilePath(default = {config.DEFAULT_OUTPUT_DIR}/output) > ")
    filename = filename if filename != '' else f"{config.DEFAULT_OUTPUT_DIR}/output"

    PlantUml(Path(filename)).write_file(logs, False)


if __name__ == '__main__':
    main()
