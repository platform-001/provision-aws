output "ecr_repo_name" {
  value = aws_ecr_repository.svc.name
}

output "ecr_repo_arn" {
  value = aws_ecr_repository.svc.arn
}

output "apprunner_service_arn" {
  value       = try(aws_apprunner_service.svc[0].arn, "")
  description = "Solo si se crea App Runner"
}

output "apprunner_service_url" {
  value       = try(aws_apprunner_service.svc[0].service_url, "")
  description = "Solo si se crea App Runner"
}
