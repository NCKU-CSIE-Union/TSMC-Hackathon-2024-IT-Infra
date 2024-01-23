run:
	python3 src/run.py --dev

build-local:
	docker build -t consumer .

build-linux:
	docker build -t consumer --platform linux/amd64 .

run-docker:
	docker run --name consumer -d consumer


.PHONY: run build-local build-linux run-docker