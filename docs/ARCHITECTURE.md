# Architectural Specification: Automated Cloud Deployment Pipeline

## 1. Execution Overview
This system provides an automated continuous delivery engine that securely packages a containerized Python application, updates a secure private ECR container registry, and dynamically creates an isolated EC2 runtime node. 

## 2. Dynamic Pipeline States
1. **Validation & Linting Phase:** GitHub Actions runner initiates Docker builds and triggers unit test suites dynamically.
2. **Registry Ingress Framework:** The script handles ECR token retrieval via OIDC token authentication, builds minimal distribution layers, and pushes images.
3. **Provisioning & Infrastructure Setup:** The infrastructure engine maps local network targets, generates structural firewalls (Security Groups), and deploys the node compute engine.
4. **Resiliency Loop Configuration:** The target EC2 runtime utilizes the native systemd execution layer to run the Docker daemon under an aggressive auto-restart constraint (`--restart always`), mitigating unexpected microservice crashes.