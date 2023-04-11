#### Install Docker
- [Follow these instructions](https://developer.hashicorp.com/terraform/downloads)

#### See Week 1 Notes
- [Follow these instructions](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/week_1_basics_n_setup/1_terraform_gcp)

#### Quickstart
- create a main.tf file (entry point for terraform)
- create a variables.tf file (variables for terraform)
- use gcloud to create a service account
  - export GOOGLE_APPLICATION_CREDENTIALS="<path/to/your/service-account-authkeys>.json"
  - aka `export GOOGLE_APPLICATION_CREDENTIALS=".secrets/gcloud.json"`

#### Terraform Commands
- `terraform init` - initialize terraform
- `terraform plan` - show what terraform will do
- `terraform apply` - apply the changes
- `terraform destroy` - destroy the changes


