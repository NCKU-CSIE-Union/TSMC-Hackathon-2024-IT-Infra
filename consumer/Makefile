run:
	python3 src/run.py --dev

build-local:
	docker build -t consumer .

build-linux:
	docker build -t consumer --platform linux/amd64 .

run-docker:
	docker run --name consumer -d consumer

auth-docker:
	gcloud auth print-access-token | docker login -u oauth2accesstoken --password-stdin https://us-central1-docker.pkg.dev

tag-docker:
	docker tag consumer  us-central1-docker.pkg.dev/tsmccareerhack2024-icsd-grp5/tsmccareerhack2024-icsd-grp5-repository/consumer 

push-docker:
	docker push us-central1-docker.pkg.dev/tsmccareerhack2024-icsd-grp5/tsmccareerhack2024-icsd-grp5-repository/consumer


.PHONY: run build-local build-linux run-docker auth-docker tag-docker push-docker