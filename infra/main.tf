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

  # App Runner solo si se pidió y hay imagen inicial
  #do_apprunner = var.crear_apprunner && length(trimspace(var.imagen_inicial)) > 0
  do_apprunner = var.crear_apprunner
}

resource "aws_ecr_repository" "svc" {
  name = local.ecr_repo_name
}

resource "aws_apprunner_service" "svc" {
  count = local.do_apprunner ? 1 : 0

  service_name = "${local.ecr_repo_name}-service"

  source_configuration {
    image_repository {
      image_identifier      = "public.ecr.aws/docker/library/nginx:latest"
      image_repository_type = "ECR_PUBLIC"

      image_configuration {
        port = "80"
      }
    }

    auto_deployments_enabled = false
  }
}
