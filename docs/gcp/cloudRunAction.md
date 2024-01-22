# GCP Cloud Run Github CI/CD
> last update : 2024.01.22

## Cloud Run CI/CD

steps : 
> can add `test` step before `build` step
1. build image
2. push image to Artifact Registry
3. deploy image to Cloud Run


## Action Setup 

> Create **Project** before setup action <br>
> https://console.cloud.google.com/projectcreate

### Required Env & Secret on Github
required env :
- `PROJECT_ID` : Google Cloud Project ID
- `GAR_LOCATION` : Artifact Registry Location ( ex: `asia-east1` )
- `GAR_REPOSITORY` : Artifact Registry Repository Name ( ex: `github-repo` )
- `SERVICE` : Cloud Run Service Name ( Instance Name )
- `REGION` : Cloud Run Region ( ex: `asia-east1` )
- `BUILD_PATH` : Build Path ( ex: `./` for root , `./backend` for backend folder )

required secret :
- `WIF_PROVIDER` : []()
  - ( ex: `projects/1234567/global/workloadIdentityPools/${POOL_NAME}/providers/github-provider` )
  > Workload Identity Pool Provider Resource Name
- `WIF_SERVICE_ACCOUNT` : []() 
  - ( ex: `{$ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com` )
  > Service Account Email

### Service API that Need to be enabled

1. Artifact Registry API
2. Cloud Build API
3. Cloud Run API

by : **GCP Console UI** or **Terminal**
- GCP Console UI

- Terminal
```
gcloud services enable artifactregistry.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
```

### Permissions to be added

> Error: ? <br>
> IAM Policy Troubleshooter

![iam-policy-troubleshooter](./docs/iam-policy-troubleshooter.png)

### Local Env Setup

set local env :
```bash
export PROJECT_ID=your-project-id # Google Cloud Project ID
export SERVICE_ACCOUNT_NAME=your-service-account-name # Service Account Name
export POOL_NAME=your-pool-name # Workload Identity Pool Name
export GITHUB_REPO=UserName/RepoName # Github Repo Name
export GAR_LOCATION=your-artifact-registry-location # Artifact Registry Location , ex: asia-east1
```

example :
```bash
export PROJECT_ID=tsmc-test-412003 # Google Cloud Project ID
export SERVICE_ACCOUNT_NAME=github-service-account # Service Account Name
export POOL_NAME=github-pool # Workload Identity Pool Name
export GITHUB_REPO=jason810496/TSMC-Hackathon-2024-IT-Infra # Github Repo Name
export GAR_LOCATION=asia-east1 # Artifact Registry Location
```

### Artifact Registry 

> make sure **already enable** Artifact Registry API
Create Artifact Registry Repository

- GCP Console UI
- Terminal
```
gcloud artifacts repositories create "github-repo" \
  --repository-format="docker" \
  --location="${GAR_LOCATION}" \
  --description="GitHub Artifact Registry Repository" \
  --project="${PROJECT_ID}"
```

> remember to create Artifact Registry Repository !!!
### Create Service Account

```
gcloud iam service-accounts create "${SERVICE_ACCOUNT_NAME}" \
  --project "${PROJECT_ID}"
```

### Create Workload Identity Pool

```
gcloud iam workload-identity-pools create "${POOL_NAME}" --project="${PROJECT_ID}" --location="global" --display-name="GitHub Deployment Pool"
```

### Set `Wordload Identity Pool Id` to `WORKLOAD_IDENTITY_POOL_ID` ( local env )

get workload identity pool id and set to env :
```
export WORKLOAD_IDENTITY_POOL_ID=$(gcloud iam workload-identity-pools describe "${POOL_NAME}" --project="${PROJECT_ID}" --location="global" --format="value(name)")
```

### Create Workload Identity Pool Provider
```
gcloud iam workload-identity-pools providers create-oidc "github-provider" \
  --project="${PROJECT_ID}" \
  --location="global" \
  --workload-identity-pool="${POOL_NAME}" \
  --display-name="Github Provider" \
  --attribute-mapping="google.subject=assertion.sub,attribute.actor=assertion.actor,attribute.repository=assertion.repository" \
  --issuer-uri="https://token.actions.githubusercontent.com"
```


### Bind Service Account to Provider
```
gcloud iam service-accounts add-iam-policy-binding "${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com" \
  --project="${PROJECT_ID}" \
  --role="roles/iam.workloadIdentityUser" \
  --member="principalSet://iam.googleapis.com/${WORKLOAD_IDENTITY_POOL_ID}/attribute.repository/${GITHUB_REPO}"
```

### Grant all required permissions to service account


#### add `uploadArtifacts` permission
> otherwise, you will get `ERROR: denied: Permission "artifactregistry.repositories.uploadArtifacts" denied`
<!-- 
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="principalSet://iam.googleapis.com/${WORKLOAD_IDENTITY_POOL_ID}/attribute.repository/${GITHUB_REPO}" \
    --role="roles/artifactregistry.admin"
 -->
```
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com" \
    --role="roles/artifactregistry.admin"
```

#### add `roles/cloudbuild.builds.builder` permission
> otherwise, you will get `ERROR: denied: Permission "artifactregistry.repositories.uploadArtifacts" denied` <br>
> https://cloud.google.com/composer/docs/troubleshooting-environment-creation#builder-permissions
<!-- 
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="principalSet://iam.googleapis.com/${WORKLOAD_IDENTITY_POOL_ID}/attribute.repository/${GITHUB_REPO}" \
    --role="roles/cloudbuild.builds.builder"
 -->
```
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com" \
    --role="roles/cloudbuild.builds.builder"
```

#### add `Cloud Run Service Agent` permission 
> otherwise, you will get `ERROR: Permission 'run.services.get' denied`
<!-- 
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="principalSet://iam.googleapis.com/${WORKLOAD_IDENTITY_POOL_ID}/attribute.repository/${GITHUB_REPO}" \
    --role="roles/run.serviceAgent"
 -->
```
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com" \
    --role="roles/run.serviceAgent"
```

### Get Provider Resource Name ( `WIF_PROVIDER` )
```
gcloud iam workload-identity-pools providers describe "github-provider" \
  --project="${PROJECT_ID}" \
  --location="global" \
  --workload-identity-pool="${POOL_NAME}" \
  --format="value(name)"
```
> return : `projects/1234567/global/workloadIdentityPools/${POOL_NAME}/providers/github-provider` <br>
> set to `WIF_PROVIDER` on Github Secret

## Secret need to be set on Github

- `WIF_PROVIDER` : 
    - eg : `projects/1234567/global/workloadIdentityPools/${POOL_NAME}/providers/github-provider`
    ```
    echo $(gcloud iam workload-identity-pools providers describe "github-provider" \
  --project="${PROJECT_ID}" \
  --location="global" \
  --workload-identity-pool="${POOL_NAME}" \
  --format="value(name)")
    ```
- `WIF_SERVICE_ACCOUNT` :
    - eg : `my-service-account@my-project.iam.gserviceaccount.com`
    ```
    echo $(${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com)
    ```


## Github Action : Cloud Run CI/CD from source ( include Build and Deploy )



original action : <br>
https://github.com/google-github-actions/example-workflows/blob/main/workflows/deploy-cloudrun/cloudrun-docker.yml

**But** , this action need to be **updated** to push image to Artifact Registry !!! <br>

Fix version : <br>

> The `docker login` part should login again using `oauth2accesstoken` with `gcloud auth print-access-token` command. <br>

## reference 

- https://medium.com/@vngauv/from-github-to-gce-automate-deployment-with-github-actions-27e89ba6add8
- https://github.com/google-github-actions/example-workflows/blob/main/workflows/deploy-cloudrun/cloudrun-docker.yaml
- https://ithelp.ithome.com.tw/articles/10313024