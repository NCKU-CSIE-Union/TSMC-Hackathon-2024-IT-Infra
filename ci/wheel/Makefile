build:
	docker build -t jasonbigcow/wheel_ci .
push:
	docker push jasonbigcow/wheel_ci
build-linux:
	docker buildx build --platform linux/amd64 -t jasonbigcow/wheel_ci:linux --push .
push-linux:
	docker push jasonbigcow/wheel_ci:linux 

build-mac:
	docker build -t jasonbigcow/wheel_ci:mac -f Dockerfile .
push-mac:
	docker push jasonbigcow/wheel_ci:mac

local-restart:
	docker build -t jasonbigcow/wheel_ci:mac -f Dockerfile .
	docker compose down
	docker compose up -d
	docker compose logs -f

compose:
	docker compose up -d
	docker compose logs -f
down:
	docker compose down

runner:
	python3 runner/run.py

init:
	mkdir logs tasks yaml 

clean-log:
	rm -rf logs/*

clean-task:
	rm -rf tasks/*

.PHONY: build build-linux push compose down runner init clean-log clean-task