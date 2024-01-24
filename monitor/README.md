# Cloud Run Monitor System

## Setup `gcloud` environment

```bash
gcloud auth application-default login
```

## Manipulate Cloud Run Service With Python SDK

### Adjust `CPU` and `Memory` of Cloud Run Service

- <https://github.com/googleapis/google-cloud-python/blob/main/packages/google-cloud-run/google/cloud/run_v2/types/service.py#L502>
- <https://github.com/googleapis/google-cloud-python/blob/main/packages/google-cloud-run/google/cloud/run_v2/types/revision_template.py#L144>
- <https://github.com/googleapis/google-cloud-python/blob/main/packages/google-cloud-run/google/cloud/run_v2/types/k8s_min.py#L164>

### Adjust `INSTANCE COUNT` of Cloud Run Service

- <https://github.com/googleapis/google-cloud-python/blob/main/packages/google-cloud-run/google/cloud/run_v2/types/service.py#L502>
- <https://github.com/googleapis/google-cloud-python/blob/main/packages/google-cloud-run/google/cloud/run_v2/types/revision_template.py#L33>
- <https://github.com/googleapis/google-cloud-python/blob/313f5672c1d16681dd4db2c4a995c5668259ea7d/packages/google-cloud-run/google/cloud/run_v2/types/vendor_settings.py#L213>

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
