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

# App Runner necesita una imagen inicial en ECR para crear el servicio.
# Para demo rápida, puedes crear el servicio manual una vez,
# o crear el servicio apuntando a una imagen placeholder si ya la tienes.

# Recomendación demo: en este TF crea ECR y deja App Runner opcional,
# y luego el pipeline del microservicio hace el primer push + update-service.
