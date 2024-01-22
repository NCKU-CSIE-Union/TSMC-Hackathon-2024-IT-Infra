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

### API to be enabled
1. Artifact Registry API
2. Cloud Build API
3. Cloud Run API

### Permissions to be added

> Error: ?
> Policy Troubleshooter


### Artifact Registry 

1. enable Artifact Registry API
2. create Artifact Registry Repository

- using terminal
```
gcloud artifacts repositories create "github-repo" \
  --repository-format="docker" \
  --location="asia-east1" \
  --description="GitHub Artifact Registry Repository" \
  --project="${PROJECT_ID}"
```

> remember to create Artifact Registry Repository !!!

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
> in local terminal
```
export PROJECT_ID=tsmc-test-412003

gcloud iam service-accounts create "github-service-account" \
  --project "${PROJECT_ID}"
```

#### Workload Identity

> in local terminal

create workload identity pool : 
```
gcloud iam workload-identity-pools create "github-pool" --project="${PROJECT_ID}" --location="global" --display-name="GitHub Deployment Pool"
```
get workload identity pool id and set to env :
```
export WORKLOAD_IDENTITY_POOL_ID=$(gcloud iam workload-identity-pools describe "github-pool" --project="${PROJECT_ID}" --location="global" --format="value(name)")
```
>get workload identity pool id
>```
>gcloud iam workload-identity-pools describe "github-pool" --project="${PROJECT_ID}" --location="global" --format="value(name)"
>```

create provider :
```
gcloud iam workload-identity-pools providers create-oidc "github-provider" \
  --project="${PROJECT_ID}" \
  --location="global" \
  --workload-identity-pool="github-pool" \
  --display-name="Github Provider" \
  --attribute-mapping="google.subject=assertion.sub,attribute.actor=assertion.actor,attribute.repository=assertion.repository" \
  --issuer-uri="https://token.actions.githubusercontent.com"
```

export Github repo name to env :
```
export GITHUB_REPO=jason810496/TSMC-Hackathon-2024-IT-Infra
# export GITHUB_REPO="USERNAME/REPO"
echo $GITHUB_REPO
```

bind service account to provider :
```
gcloud iam service-accounts add-iam-policy-binding "github-service-account@${PROJECT_ID}.iam.gserviceaccount.com" \
  --project="${PROJECT_ID}" \
  --role="roles/iam.workloadIdentityUser" \
  --member="principalSet://iam.googleapis.com/${WORKLOAD_IDENTITY_POOL_ID}/attribute.repository/${GITHUB_REPO}"
```

add `uploadArtifacts` permission :
```
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="principalSet://iam.googleapis.com/${WORKLOAD_IDENTITY_POOL_ID}/attribute.repository/${GITHUB_REPO}" \
    --role="roles/artifactregistry.admin"
  
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:github-service-account@${PROJECT_ID}.iam.gserviceaccount.com" \
    --role="roles/artifactregistry.admin"
```

add `roles/cloudbuild.builds.builder` permission to service account :
> otherwise, you will get `ERROR: denied: Permission "artifactregistry.repositories.uploadArtifacts" denied`
> https://cloud.google.com/composer/docs/troubleshooting-environment-creation#builder-permissions
```
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="principalSet://iam.googleapis.com/${WORKLOAD_IDENTITY_POOL_ID}/attribute.repository/${GITHUB_REPO}" \
    --role="roles/cloudbuild.builds.builder"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:github-service-account@${PROJECT_ID}.iam.gserviceaccount.com" \
    --role="roles/cloudbuild.builds.builder"
```

add `Cloud Run Service Agent` permission to service account :
> otherwise, you will get `ERROR: Permission 'run.services.get' denied`
```
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="principalSet://iam.googleapis.com/${WORKLOAD_IDENTITY_POOL_ID}/attribute.repository/${GITHUB_REPO}" \
    --role="roles/run.serviceAgent"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:github-service-account@${PROJECT_ID}.iam.gserviceaccount.com" \
    --role="roles/run.serviceAgent"
```

**Final** : get provider resource name :
```
gcloud iam workload-identity-pools providers describe "github-provider" \
  --project="${PROJECT_ID}" \
  --location="global" \
  --workload-identity-pool="github-pool" \
  --format="value(name)"
```
> return : `projects/1234567/global/workloadIdentityPools/github-pool/providers/github-provider`
> Github Secret : `WIF_PROVIDER`

#### Set Service Account Key to Github Secret

- `WIF_PROVIDER` : **Final** : get provider resource name
    - `projects/1234567/global/workloadIdentityPools/github-pool/providers/github-provider`
- `WIF_SERVICE_ACCOUNT` :
    - > `my-service-account@my-project.iam.gserviceaccount.com`
    - > `github-service-account@${PROJECT_ID}.iam.gserviceaccount.com`



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

----

