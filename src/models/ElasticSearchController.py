# coding: utf-8
from re import compile, sub
from typing import List
from pathlib import Path
from subprocess import run
from datetime import datetime
from pprint import pprint
from elasticsearch import Elasticsearch


class ElasticSearchController(object):
    def __init__(self, index_name: str):
        self.es = Elasticsearch()
        self.index_name = index_name

    def search(self, query: dict):
        return self.es.search(index=self.index_name, body=query, size=100, sort='body.@timestamp').get('hits').get('hits')

    def search_and_filter(self, filters: list):
        return self.search(query={
            "query": {
                "bool": {
                    "filter": filters
                }
            }
        })

    def search_by_eventids(self, eventids: List[int]):
        return self.search(query={
            "query": {
                "terms": {
                    "body.Event.System.EventID.#text": eventids
                }
            }
        })


def get_dict(source: dict, query: str):
    result = source
    for q in query.split('.'):
        try:
            result.get(q)
            result = result.get(q)
        except Exception:
            return result
    return result


if __name__ == '__main__':

    es = ElasticSearchController('_all')

    detect_malware = (es.search_by_eventids(eventids=[1116, 1117]))

    logon = es.search_and_filter(filters=[
        {"terms": {"body.Event.System.EventID.#text": [4624]}},
        {"term": {"body.Event.EventData.Data.LogonType": 10}}
    ])

    logoff = (es.search_by_eventids(eventids=[4634]))

    failed_logon = (es.search_by_eventids(eventids=[4634]))

    #result = detect_malware + logon + logoff
    result = logon
    
    text = ''
    filename = input('input filepath> ')

    pattern = compile(r'T.*')

    date = ''
    for i in result:
        
        if sub(pattern, '', get_dict(i, '_source.body.@timestamp')) != date:
            text += f"== {get_dict(i, '_source.body.@timestamp').replace('T',' ')} ==\n"

        text += '\n'.join([
            f"{get_dict(i, '_source.body.Event.EventData.Data.IpAddress')} -> {get_dict(i, '_index')}: LOGON / {get_dict(i, '_source.body.Event.EventData.Data.TargetUserName')}",
            f"activate {get_dict(i, '_index')}",
            '',
        ])
        date = sub(pattern, '', get_dict(i, '_source.body.@timestamp'))

    #get_dict(i, '_source.body.Event.System.Computer'),
    #get_dict(i, '_source.body.Event.EventData.Data.TargetDomainName'),
    #get_dict(i, '_source.body.Event.EventData.Data.LogonProcessName'),

    header = '\n'.join([
        '@startuml',
        '',
        'skinparam monochrome true',
        'skinparam defaultFontName Arial',
        'skinparam ParticipantPadding 50',
        'hide footBox',
        '\n',
    ])
    footer = '\n@enduml'

    Path(filename + '.uml').write_text(header + text + footer)
    run(['plantuml', filename + '.uml'])
    #pprint(get_dict(i, 'body.Event.EventData.Data.LogonType'))

# actor User
# participant "First Class" as A
# participant "Second Class" as B
# participant "Last Class" as C
# User -> A: DoWork
# activate A
# == 2019.06.05 ==
# A -> B: Create Request
# note over of A: hoge
# deactivate A
# B -> C: DoWork
