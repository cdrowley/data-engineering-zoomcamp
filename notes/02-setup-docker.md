## Install Docker
- [Follow these instructions](https://docs.docker.com/install/)

## Check Docker Works
`docker --version`
`docker run hello-world`

## Create a Dockerfile
`touch Dockerfile`

## Use Python Docker Image
`docker run -it --entrypoint /bin/bash python:3.9`

## Create a Custom Docker Image
- Create a `Dockerfile` in the root of your project
- Copy the contents of the `Dockerfile` in this repo

## Build the Docker Image
`docker build -t test:pandas .`

## Run the Docker Image
`docker run -it test:pandas`