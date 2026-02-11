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
  # ECR repo name: sanitizado para ECR (minúsculas, ':' -> '-')
  ecr_repo_name = lower(replace(var.cod_servicio, ":", "-"))

  # App Runner solo si se pidió
  do_apprunner = var.crear_apprunner
}

resource "aws_ecr_repository" "svc" {
  name         = local.ecr_repo_name
  force_delete = true
}

# Role para que App Runner pueda acceder a ECR privado (pull)
resource "aws_iam_role" "apprunner_ecr_access" {
  count = local.do_apprunner ? 1 : 0
  name  = "${local.ecr_repo_name}-apprunner-ecr-access"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect = "Allow",
      Principal = {
        Service = "build.apprunner.amazonaws.com"
      },
      Action = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy_attachment" "apprunner_ecr_access" {
  count      = local.do_apprunner ? 1 : 0
  role       = aws_iam_role.apprunner_ecr_access[0].name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSAppRunnerServicePolicyForECRAccess"
}

resource "aws_apprunner_service" "svc" {
  count = local.do_apprunner ? 1 : 0

  service_name = "${local.ecr_repo_name}-service"

  source_configuration {
    # 👇 CLAVE: App Runner necesita este access role para ECR privado
    authentication_configuration {
      access_role_arn = aws_iam_role.apprunner_ecr_access[0].arn
    }

    image_repository {
      # var.imagen_inicial aquí debe ser un TAG existente (ej: "bootstrap")
      image_identifier      = "${aws_ecr_repository.svc.repository_url}:${var.imagen_inicial}"
      image_repository_type = "ECR"

      image_configuration {
        port = "8080"
      }
    }

    auto_deployments_enabled = false
  }

  depends_on = [aws_iam_role_policy_attachment.apprunner_ecr_access]
}
