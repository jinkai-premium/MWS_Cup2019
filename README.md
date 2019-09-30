# JFAP(JINKAI Forensics Analyzer PREMIUM)
Log visualization tool for investigating the damage caused by cyber attacks.


## Demo
![68747470733a2f2f692e6779617a6f2e636f6d2f35383065333565326330636132333661346139363934316162343736393730642e706e67](https://user-images.githubusercontent.com/55793713/65867901-32f34b80-e3b2-11e9-8106-d8efc163cecf.png)


## Description
In the digital forensics, in general, the damage from a cyber-attack is investigated using tools corresponding to each log, and the complete picture of the attack is grasped by collecting the obtained information.\
\
However, the general method takes a lot of time to get the complete picture so that it is not suitable for understanding the detailed overview of it.\
\
Therefore, this tool supports the damage investigation of cyber-attacks based on the knowledge from the log analyses that have been done manually, and by providing a function to visualize the detailed overview of the complete picture from logs.


## Functions
1. Filtering function
    - Time stamp tampering detection (Unimplemented)
    
    - Detection of writing a large number of files (Unimplemented)
  
    - Detection of time stamp outliers in each directory (Unimplemented)

    - Malware detection using the Prefech function (Unimplemented)

    - Record of unauthorized remote logon

2. The function for displaying the timeline of filtering result


## Requirements
- Linux / macOS / WSL
- Python: 3.6.5+
- Docker: latest
- Docker-compose: latest 


## Installation
### via pip(Recommended)
```bash
$ pip install git+https://github.com/jinkai-premium/MWS_Cup2019

# IMPORTANT: Bulk-indice your evtx files to elasticsearch(default: localhost:9200).
#            In each run after the first, you should not be add `--input` option(it does not indices from evtx files).
$ mwscup2019_jinkai-premium --input="/path/to/your/evtx/directory"

# Other options:
#   --output: output filepath(default: dist/out.uml, dist/out.png)
#   --nopng : not to generate png image(use when `docker` doesn't work environment.)
```

### manually install
```bash
$ git clone https://github.com/jinkai-premium/MWS_Cup2019
$ cd MWS_Cup2019

$ sh scripts/docker_elk.sh
# or run `docker-compose up` on /src/scripts/

$ python -m .venv venv
$ source .venv/bin/activate
$ pip install -r requirements.txt

$ python scripts/indices_evtxfiles.py {/path/to/your/evtx/directory}
```


## Usage
### via pip(Recommended)
```bash
$ mwscup2019_jinkai-premium
```

### manually install
```bash
$ python src/run.py
```


## License
[MIT](https://github.com/jinkai-premium/MWS_Cup2019/blob/master/LICENSE)
