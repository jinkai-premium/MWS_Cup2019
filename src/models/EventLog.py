# coding: utf-8
from typing import List


class EventLog(object):
    def __init__(self, raw: dict) -> None:
        self.id = get_dict(raw, '_id')
        self.index = get_dict(raw, '_index')
        self.timestamp = get_dict(raw, '_source.body.@timestamp').replace('T', ' ').split('.')[0]
        self.event_id = get_dict(raw, '_source.body.Event.System.EventID.#text')


class EventLog_Logon(EventLog):
    def __init__(self, raw: dict) -> None:
        super().__init__(raw)
        self.ip_address = get_dict(raw, '_source.body.Event.EventData.Data.IpAddress')
        self.target_name = get_dict(raw, '_source.body.Event.EventData.Data.TargetUserName')
        self.logon_id = get_dict(raw, '_source.body.Event.EventData.Data.TargetLogonId')


class EventLog_Logoff(EventLog):
    def __init__(self, raw: dict, logon_list: List[EventLog]) -> None:
        super().__init__(raw)
        self.logon_id = get_dict(raw, '_source.body.Event.EventData.Data.TargetLogonId')
        self.parent_id = self.trace_parent(logon_list)

    def trace_parent(self, logon_list):
        for logon in logon_list:
            if logon.logon_id == self.logon_id:
                return logon.ip_address


class EventLog_DetectMalware(EventLog):
    def __init__(self, raw: dict) -> None:
        super().__init__(raw)
        self.malware_type = get_dict(raw, '_source.body.Event.EventData.RawData').split('<string>')[8].split('</string>')[0]


def get_dict(source: dict, query: str):
    result = source
    for q in query.split('.'):
        try:
            result.get(q)
            result = result.get(q)
        except Exception:
            return result
    return result
