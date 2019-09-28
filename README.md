# README

## demo
![](https://i.gyazo.com/580e35e2c0ca236a4a96941ab476970d.png)

## dependency
linux/macOS/WSL

## require
- Python: >=3.6.5
- docker: latest
- docker-compose: latest

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