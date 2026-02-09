terraform {
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 5.0" }
  }
}

provider "aws" {
  region = var.region
}

resource "aws_ecr_repository" "svc" {
  name = var.cod_servicio
}

# App Runner: lo creamos SOLO si crear_apprunner=true y hay imagen_inicial
locals {
  do_apprunner = var.crear_apprunner && length(var.imagen_inicial) > 0
}

resource "aws_apprunner_service" "svc" {
  count = local.do_apprunner ? 1 : 0

  service_name = "${var.cod_servicio}-service"

  source_configuration {
    image_repository {
      image_identifier      = var.imagen_inicial
      image_repository_type = "ECR"

      image_configuration {
        port = "8080"
      }
    }

    auto_deployments_enabled = false
  }
}
