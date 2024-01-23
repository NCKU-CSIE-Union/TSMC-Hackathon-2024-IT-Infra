# Cloud Run Monitor System

## Setup `gcloud` environment

```bash
gcloud auth application-default login
```

## Reference

### Cloud Run API

- [sdk pipy](https://pypi.org/project/google-cloud-run/)
- [github](https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-run)
- [gcloud commad list](https://cloud.google.com/sdk/gcloud/reference/run)
- [gcloud update reference](https://cloud.google.com/sdk/gcloud/reference/run/services/update)
- python call `gcloud run service update` directly

### Cloud Run Log and Metrics Retrieve API

#### Logging API

- [python sdk for logging](https://cloud.google.com/logging/docs/reference/libraries#client-libraries-install-python)
- [cloud run logging api](https://cloud.google.com/run/docs/logging)

#### Metrics API

- [cloud run metrics api](https://cloud.google.com/monitoring/api/metrics_gcp#gcp-run)
- [python sdk for metrics](https://cloud.google.com/monitoring/docs/reference/libraries#client-libraries-install-python)