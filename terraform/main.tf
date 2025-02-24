terraform {
  required_providers {
    aws = {
        source = "hashicorp/aws"
        version = "~> 5.0"
    }
  }
   backend "s3" {
    bucket = "totes-tf-states"
    key = "/terraform.tfstate"
    region = var.region_name
  }
}
provider "aws" {
  region = var.region_name
  default_tags {
    tags = {
        project = "tote piping"
        user = "coad team"
    }
  }
}

data "aws_caller_identity" "current" {}

data "aws_region" "current" {}