variable "cod_servicio" { type = string }
variable "region" { type = string }

variable "crear_apprunner" {
  type    = bool
  default = true
}

variable "imagen_inicial" {
  type    = string
  default = "bootstrap"
}
