variable "cod_servicio" { type = string }
variable "region" { type = string }

variable "crear_apprunner" {
  type    = bool
  default = false
}

variable "imagen_inicial" {
  type    = string
  default = ""
}
