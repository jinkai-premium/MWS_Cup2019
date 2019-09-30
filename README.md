# README

## dependency
linux/macOS/WSL

## require
- Python: >=3.6.5
- docker: latest
- docker-compose: latest

## console-run(recommended)
```
$ pip install https://github.com/jinkai-premium/MWS_Cup2019

# IMPORTANT: bulk-indice your evtx files to elasticsearch(default: localhost:9200)
$ mwscup2019_jinkai-premium --input="/path/to/your/evtx/directory"
```

## run
```
$ git clone https://github.com/jinkai-premium/MWS_Cup2019
$ cd MWS_Cup2019

$ sh scripts/docker_elk.sh

$ python -m .venv venv
$ source .venv/bin/activate
$ pip install -r requirements.txt

$ python scripts/indices_evtxfiles.py {/path/to/your/evtx/directory}
```

```
$ python src/run.py
```
