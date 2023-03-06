
## Working Notes
docker build -t test:pandas .
docker run -it test:pandas 2022-01-01
docker ps

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
