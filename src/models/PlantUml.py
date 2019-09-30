# coding: utf-8
from typing import List
from subprocess import check_output
from pathlib import Path, PosixPath
from functools import singledispatch

from src.models.EventLog import EventLog_Logon, EventLog_Logoff, EventLog_DetectMalware
from src.models.Types import EventLogs


class PlantUml(object):
    def __init__(self, path: PosixPath) -> None:
        self.header = '\n'.join([
            '@startuml',
            'skinparam monochrome true',
            'skinparam defaultFontName Arial',
            'skinparam ParticipantPadding 50',
            'hide footBox',
            '\n',
        ])
        self.footer = '\n@enduml'
        self.path = path

    def sort_logs(self, logs: EventLogs) -> EventLogs:
        return sorted(logs, key=lambda log: log.timestamp)

    def write_file(self, logs: EventLogs, nopng: bool) -> None:
        logs = self.sort_logs(logs)

        date = ''
        text_logs: List[str] = []
        previous_msg = ''
        for log in logs:
            # if change date
            if self.get_date(log.timestamp) != date:
                text_logs.append(f"== {self.get_date(log.timestamp)} ==")

            text = parse_text(log)

            # if change text
            if previous_msg != text:
                text_logs.append(text)

            # for check distinct
            previous_msg = text
            date = self.get_date(log.timestamp)

        # sort servernames
        aliases = sorted(list({log.ip_address for log in logs if type(log) is EventLog_Logon}))
        servers = sorted(list({name.index for name in logs}))
        servers.extend(aliases)
        server_names = '\n'.join([f"participant {name}" for name in servers]) + '\n'

        text = '\n'.join(text_logs)
        Path(self.path.with_suffix('.uml')).write_text(self.header + server_names + text + self.footer)

        if not nopng:
            check_output(f"cat {self.path.with_suffix('.uml')} | docker run --rm -i think/plantuml -tpng > {self.path.with_suffix('.png')} ", shell=True)

    def get_date(self, timestamp: str) -> str:
        return timestamp.split(' ')[0]


@singledispatch
def parse_text(log):
    raise TypeError


@parse_text.register(EventLog_Logon)
def parse_logon(log) -> str:
    return f"{log.ip_address} -> {log.index}: LOGON/{log.target_name} ({log.timestamp[11:]})\nactivate {log.index}"


@parse_text.register(EventLog_Logoff)
def parse_logoff(log) -> str:
    return f"{log.index} -> {log.parent_id}: LOGOFF ({log.timestamp[11:]})\ndeactivate {log.index}"


@parse_text.register(EventLog_DetectMalware)
def parse_detectmalware(log) -> str:
    msg = 'DetectMalware' if log.event_id == '1116' else 'ActivateProtection'
    return f"note over of {log.index}: {msg}/{log.malware_type} ({log.timestamp[11:]})"
