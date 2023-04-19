
## Working Notes
docker build -t test:pandas .
docker run -it test:pandas 2022-01-01
docker ps
DockerFile:
```
FROM python:3.11

RUN pip install --upgrade pip
RUN pip install pandas

WORKDIR /app
COPY pipeline.py pipeline.py

ENTRYPOINT [ "python", "pipeline.py" ]
```

pipeline.py:
```
import sys
import pandas as pd


if len(sys.argv) > 1:
    day = sys.argv[1]
    print(f'Job finished successfully for {=day}')
```

#### Run a local python web server, to serve the files in the current directory
python -m http.server 8080

##### use pgcli to connect to postgres:
pgcli -h localhost -p 5432 -U postgres -d ny_taxi


#### Generate SSH Key
- ssh-keygen -t rsa -f ~/.ssh/xyzxyz -C xyzxyz -b 2048
- cat /Users/clivedrowley/.ssh/xyzxyz.pub
### Connect to a remote server
- copy the public key to the remote server (metadata on gcp vm)
- ssh -i ~/.ssh/xyzxyz xyzxyz@vm.external.ip.address
- useful cmds:
  - htop
  - gcloud --version

Can save a config at `~/.ssh/config` and use `ssh nyc-taxi-data-dez`
```
Host nyc-taxi-data-dez
    HostName vm.external.ip.address
    User xyzxyz
    IdentityFile ~/.ssh/xyzxyz
```
- Install Docker `sudo apt-get install docker.io`
- Install Docker Compose `sudo apt-get install docker-compose` 
  - or `wget` from gh releases
  - `chmod +x` to make it executable
  - `nano .bashrc` and add `export PATH="${HOME}/bin:${PATH}"`



