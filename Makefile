.PHONY: build clean save

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
