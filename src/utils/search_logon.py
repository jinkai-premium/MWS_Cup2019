# coding: utf-8
from models.ElasticSearchController import ElasticSearchController

def search_logon():
    return ElasticSearchController().search({
        "query": {
            "match": {
                "body.Event.System.EventID.#text": 4624
            }
        }
    })
