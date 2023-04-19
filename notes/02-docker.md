#### What is Docker?
- Docker is a set of platform as a service products that use OS-level virtualization to deliver software in packages called containers.
- Docker is a tool designed to make it easier to create, deploy, and run applications by using containers.

#### Install Docker
- [Follow these instructions](https://docs.docker.com/install/)

#### Check Docker Works
- `docker --version`
- `docker run hello-world`

#### Create a Dockerfile
- `touch Dockerfile`

#### Use Python Docker Image
- `docker run -it --entrypoint /bin/bash python:3.9`

#### Create a Custom Docker Image
- Create a `Dockerfile` in the root of your project
- Copy the contents of the `Dockerfile` in this repo

#### Build a Docker Image
`docker build -t test:pandas .`

#### Run a Docker Image
`docker run -it test:pandas`

<br>
----------------
----------------
<br>
## Manual Docker Compose (Command Line Docker)
### Setup a Shared Network
- This allows different containers to talk to each other
- `docker network create pg-network`

### Postgres Container
```
docker run -it \
-e POSTGRES_USER=postgres \
-e POSTGRES_PASSWORD=postgres \
-e POSTGRES_DB=ny_taxi \
-p 5432:5432 \
-v $(pwd)/data:/var/lib/postgresql/data \
--network pg-network \
--name db \
postgis/postgis:latest
```

### PGAdmin Container
```
docker run -it \
-e PGADMIN_DEFAULT_EMAIL=postgres@postgres.postgres \
-e PGADMIN_DEFAULT_PASSWORD=postgres \
-p 8080:80 \
--network pg-network \
dpage/pgadmin4:latest
```

### Custom Python Container
Build the image 
```
docker build -t upload-trips:v001 .
```

Run the image, in interactive mode, passing in command lines arguments to the python script:
```
export URL=https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2022-01.parquet

docker run -it --network pg-network \
    upload-trips:v001 \
        --drivername="postgresql+psycopg2" \
        --username="postgres" \
        --password="postgres" \
        --host="db" \
        --port="5432" \
        --database="postgres" \
        --table_name="yellow_taxi_trips" \
        --url=${URL}
```
