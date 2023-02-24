
docker build -t test:pandas .
docker run -it test:pandas 2022-01-01

docker ps

docker run -it \
    -e POSTGRES_USER=postgres \
    -e POSTGRES_PASSWORD=postgres \
    -e POSTGRES_DB=ny_taxi \
    -p 5432:5432 \
    -v $(pwd)/data:/var/lib/postgresql/data \
    postgres:15.2

pgcli -h localhost -p 5432 -U postgres -d ny_taxi

# pip install pgcli to work with postgres in terminal