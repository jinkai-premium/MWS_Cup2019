# hit-parser

## Query

### Remote-Logon
```
GET _search
{
  "query": {
    "match": {
      "body.Event.EventData.Data.LogonType.keyword": "10"
    }
  }
}
```