.PHONY: fresh build save _create_env up down clean

### Local Python Environment ###
fresh:
	$(MAKE) _create_venv REQUIREMENTS=requirements.in
build:
	$(MAKE) _create_venv REQUIREMENTS=requirements.txt
save:
	venv/bin/pip freeze > requirements.txt

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
	docker system prune -f
	docker-compose stop
	docker rmi `docker images -a -q`
