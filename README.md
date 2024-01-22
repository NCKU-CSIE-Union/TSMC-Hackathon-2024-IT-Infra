# TSMC-Hackathon-2024-IT-Infra


## Cloud Run CI/CD

> reference : https://medium.com/@vngauv/from-github-to-gce-automate-deployment-with-github-actions-27e89ba6add8

### Google Cloud Project

https://console.cloud.google.com/projectcreate

set project name

> Archived : use `Artifact Registry` instead of `Container Registry` 👇
> ### Container Registry API Enable
>
> search `container registry` on top search bar

### Artifact Registry 

enable Artifact Registry API

### Auth

two ways to auth
1. Service Account
2. Workload Identity

> Service Account is **much easier** to setup !!!


### IAM

setup service account permission
1. create service account
    - using terminal
    - using GCP console UI
2. create service account key
3. download service account key
4. set service account key to github secret

#### Create Service Account
1. using terminal
> in local terminal
```
export PROJECT_ID=tsmc-test-412003

gcloud iam service-accounts create "github-service-account" \
  --project "${PROJECT_ID}"
```

2. using GCP console UI

#### Create Service Account Key

> both are easy to do

1. using terminal
> in local terminal
```
gcloud iam service-accounts keys create "github-service-account.json" \
  --project "${PROJECT_ID}" \
  --iam-account "github-service-account@${PROJECT_ID}.iam.gserviceaccount.com"
```

2. using GCP console UI

#### Workload Identity

> in local terminal

create workload identity pool : 
```
gcloud iam workload-identity-pools create "github-pool"
  --project="${PROJECT_ID}" \
  --location="global" \
  --display-name="GitHub Deployment Poll"
```
get workload identity pool id : 
```
gcloud iam workload-identity-pools describe "github-pool" \
  --project="${PROJECT_ID}" \
  --location="global" \
  --format="value(name)"
```
> return : `projects/111111111/locations/global/workloadIdentityPools/my-pool`


## Github Action : Cloud Run CI/CD from source ( include Build and Deploy )

https://github.com/google-github-actions/example-workflows/blob/main/workflows/deploy-cloudrun/cloudrun-source.yml

### env setup

```
PROJECT_ID: tsmc-test-412003 # TODO: update Google Cloud project id
SERVICE: stateless-service # TODO: update Cloud Run service name
REGION: asia-east1 # TODO: update Cloud Run region
```
- PROJECT_ID : Google Cloud Project ID
- SERVICE : Cloud Run Service Name to be set
- REGION : https://cloud.google.com/compute/docs/regions-zones
