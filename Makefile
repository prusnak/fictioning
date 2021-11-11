all:
	@echo "flask  : server | dev | prod"
	@echo "docker : build | run"

server:
	FLASK_APP=server flask run

dev:
	FLASK_ENV=development FLASK_APP=server flask run

prod:
	gunicorn --bind 0.0.0.0:8080 --workers 5 --timeout 240 wsgi:app

schedule:
	python3 scheduler.py

DOCKER_IMAGE=fictioning

build:
	docker build -t $(DOCKER_IMAGE) .

run:
	docker run -p 5000:5000 --rm -it --gpus all --shm-size=1g --ulimit memlock=-1 --ulimit stack=67108864 -v $(shell pwd):/workspace $(DOCKER_IMAGE) /bin/bash
