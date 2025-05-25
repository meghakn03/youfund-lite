terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 2.20"
    }
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  required_version = ">= 1.0"
}
provider "docker" {}

variable "db_username" {
  default = "postgres"
}

variable "db_password" {
  default = "your-secure-password"
}

variable "db_name" {
  default = "youfund"
}
