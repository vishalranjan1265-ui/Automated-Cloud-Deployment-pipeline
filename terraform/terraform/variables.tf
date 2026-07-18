variable "aws_region" {
  type        = string
  description = "Target geographical deployment zone location identifier."
  default     = "us-east-1"
}

variable "environment" {
  type        = string
  description = "Operational isolation layer context label specification."
  default     = "production"
}

variable "instance_type" {
  type        = string
  description = "Hardware scale parameter allocation matrix value."
  default     = "t2.micro"
}