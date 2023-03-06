.PHONY: fresh build clean save up down

### Local Python Environment ###
fresh:
	make clean; \
	set -e; \
	python -m venv venv; \
	source venv/bin/activate; \
	pip install --upgrade pip; \
	pip install -r requirements.in;
build:
	set -e; \
	make clean; \
	python -m venv venv; \
	source venv/bin/activate; \
	pip install --upgrade pip; \
	pip install -r requirements.txt;
clean:
	rm -rf venv;
save:
	pip freeze > requirements.txt;


### Docker Environment ###
up:
	docker-compose up -d --build;
down:
	docker-compose down;
