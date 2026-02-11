terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {}
}


provider "aws" {
  region = var.region
}

locals {
  # ECR repo name: por microservicio (sin branch), sanitizado para ECR
  # - minúsculas
  # - ':' -> '-'
  ecr_repo_name = lower(replace(var.cod_servicio, ":", "-"))
}

resource "aws_ecr_repository" "svc" {
  name = local.ecr_repo_name
  force_delete = true
}

