data "aws_vpc" "default_network" {
  default = true
}

resource "aws_security_group" "pipeline_sg" {
  name        = "terraform-auto-deploy-sg"
  description = "Enforces dynamic structural validation block rules for app layers."
  vpc_id      = data.aws_vpc.default_network.id

  ingress {
    description = "Application Ingress Access Endpoint Port"
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "Administrative Cryptographic Access Channel Tunnel"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    description = "Outbound Unrestricted Resolution Paths Gate"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "Pipeline-Managed-Security-Boundary"
    Environment = var.environment
  }
}

resource "aws_ecr_repository" "app_registry" {
  name                 = "cloud-auto-deploy-app"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    DeploymentMode = "Automated-Pipeline"
    Environment    = var.environment
  }
}