all:
	@echo "prepare : prepare"
	@echo "docker  : build | run"
	@echo "flask   : server | dev | prod"
	@echo "sched   : sched"

server:
	FLASK_APP=server flask run

dev:
	FLASK_ENV=development FLASK_APP=server flask run

prod:
	gunicorn --bind 0.0.0.0:8080 --workers 5 --timeout 240 wsgi:app

sched:
	python3 scheduler.py

DOCKER_IMAGE=fictioning

build:
	docker build -t $(DOCKER_IMAGE) .

run:
	docker run -p 8080:8080 --rm -it --gpus all --shm-size=1g --ulimit memlock=-1 --ulimit stack=67108864 -v $(shell pwd):/workspace $(DOCKER_IMAGE) /usr/bin/tmux

prepare:
	mkdir -p .cache jobs
	git submodule update --init
	cd VQGAN-CLIP ; patch -p1 < ../patches/vqgan-clip.patch
	cd VQGAN-CLIP ; git clone https://github.com/openai/CLIP
	cd VQGAN-CLIP ; git clone https://github.com/CompVis/taming-transformers
	mkdir -p VQGAN-CLIP/checkpoints
	curl -L -o VQGAN-CLIP/checkpoints/vqgan_imagenet_f16_16384.yaml -C - 'https://heibox.uni-heidelberg.de/d/a7530b09fed84f80a887/files/?p=%2Fconfigs%2Fmodel.yaml&dl=1'
	curl -L -o VQGAN-CLIP/checkpoints/vqgan_imagenet_f16_16384.ckpt -C - 'https://heibox.uni-heidelberg.de/d/a7530b09fed84f80a887/files/?p=%2Fckpts%2Flast.ckpt&dl=1'
