access-token:
	gcloud auth print-access-token 

access-token-env:
	printf "ACCESS_TOKEN=" > .env/dev.env
	gcloud auth print-access-token >> .env/dev.env

sdk-auth-init:
	gcloud auth application-default login 


.PHONY: access-token