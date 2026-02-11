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
  force_delete = true
}

resource "aws_apprunner_service" "svc" {
  count = local.do_apprunner ? 1 : 0

  service_name = "${local.ecr_repo_name}-service"

  source_configuration {
    image_repository {
      image_identifier      = "${aws_ecr_repository.svc.repository_url}:${var.imagen_inicial}"
      image_repository_type = "ECR"

      image_configuration {
        port = "8080"
      }
    }

    auto_deployments_enabled = false
  }
}
