## Create a GCP Account
- [Follow these instructions](https://cloud.google.com/free/docs/gcp-free-tier)

## Create a GCP Bucket for the NYC Taxi Data
- [Follow these instructions](https://cloud.google.com/storage/docs/creating-buckets)
- Give the bucket a logical name, e.g. `nyc-taxi-data`
- Bucket names are globally unique, so add a suffix. For example, `nyc-taxi-data-john`

## Install Google Cloud SDK
- [Follow these instructions](https://cloud.google.com/sdk/docs/install-sdk)

# Check Google Cloud SDK Works
- `gcloud init`

## Create a Service Account & Download Credentials
- [Follow these instructions](https://cloud.google.com/iam/docs/creating-managing-service-accounts)

# Export Credentials & Check Authentication
- `export GOOGLE_APPLICATION_CREDENTIALS="<path/to/your/service-account-authkeys>.json"`
- `gcloud auth application-default login`
