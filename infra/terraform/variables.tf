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

# Currently unused, but helpful for future scalability
variable "bucket_name" {
  description = "The name of the S3 bucket to create"
  type        = string
  default     = "youfund-data"
}
