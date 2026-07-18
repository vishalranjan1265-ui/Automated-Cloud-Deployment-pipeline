# Technical Design Specification: Orchestration Parameters

## 1. Network Boundary Mapping
The instance is provisioned into the default VPC boundary inside the designated active AWS execution region. Ingress parameters match structural traffic isolation frameworks:

- **TCP Port 8080:** Public internet routing entry path targeting the containerized Flask app interface.
- **TCP Port 22:** Restrictive SSH administration interface channel.

## 2. Bootstrapping UserData Core Logics
The machine initialization script executes sequentially during first-boot parameters:
- System package optimization and Docker Engine daemon assembly.
- ECR regional registry credential token injection.
- Execution block deployment using runtime monitoring options (`-d --name web-app-prod`).