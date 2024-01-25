# setup cloud run
# Usage: setup.sh <project_id> <service_account_name> <workload_identity_pool_name> <github_repo> <artifact_registry_location>

set -e
PROJECT_ID=$1
SERVICE_ACCOUNT_NAME=$2
WORKLOAD_IDENTITY_POOL_NAME=$3
GITHUB_REPO=$4