.PHONY: fresh build save _create_env up down clean


### Local Python Environment ###
fresh:
	$(MAKE) _create_venv REQUIREMENTS=requirements.in;
build:
	$(MAKE) _create_venv REQUIREMENTS=requirements.txt;
save:
	venv/bin/pip freeze > requirements.txt;
_create_venv:
	rm -rf venv; \
	set -e; \
	python -m venv venv; \
	source venv/bin/activate; \
	pip install --upgrade pip; \
	pip install -r $(REQUIREMENTS);


### Docker Environment ###
up:
	docker-compose up -d --build;
down:
	docker-compose down;
clean:
	docker system prune -f; \
	docker-compose stop; \
	docker rmi `docker images -a -q`;
data:
	$(MAKE) up; \
	docker build -t upload-trips:v001 .; \
	export URL=https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2022-01.parquet; \
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
