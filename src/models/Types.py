# coding: utf-8
from typing import List, Union
from src.models.EventLog import EventLog, EventLog_Logon, EventLog_Logoff

EventLogs = List[Union[EventLog, EventLog_Logon, EventLog_Logoff]]
