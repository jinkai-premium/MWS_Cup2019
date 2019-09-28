# coding: utf-8
from typing import List

from elasticsearch import Elasticsearch

from models.Config import Config


class ElasticSearchController(object):
    def __init__(self, index_name: str) -> None:
        c = Config()
        self.es = Elasticsearch(f"{c.ELASTICSEARCH_HOST}:{c.ELASTICSEARCH_PORT}")
        self.index_name = index_name

    def search(self, query: dict) -> dict:
        return self.es.search(index=self.index_name, body=query, size=100, sort='body.@timestamp').get('hits').get('hits')

    def search_and_filter(self, filters: list) -> dict:
        return self.search(query={
            "query": {
                "bool": {
                    "filter": filters
                }
            }
        })

    def search_by_eventids(self, eventids: List[int]) -> dict:
        return self.search(query={
            "query": {
                "terms": {
                    "body.Event.System.EventID.#text": eventids
                }
            }
        })
