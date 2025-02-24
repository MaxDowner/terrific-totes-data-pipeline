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
    region = "eu-west-2"
  }
}
provider "aws" {
  region = "eu-west-2"
  default_tags {
    tags = {
        project = "tote piping"
        user = "coad team"
    }
  }
}

data "aws_caller_identity" "current" {}

data "aws_region" "current" {}