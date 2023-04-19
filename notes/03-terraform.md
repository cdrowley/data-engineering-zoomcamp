#### What is Terraform?
- Terraform is an open-source infrastructure as code software tool created by HashiCorp. Users define and provide data center infrastructure using a declarative configuration language known as HashiCorp Configuration Language, or optionally JSON.
- Terraform can manage existing and popular service providers as well as custom in-house solutions.
- Terraform is a tool for building, changing, and versioning infrastructure safely and efficiently.

#### Install Terraform
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


