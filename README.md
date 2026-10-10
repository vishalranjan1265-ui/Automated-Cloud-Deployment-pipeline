## Automated Cloud Deployment Pipeline
Built to understand how deployment automation and security checks fit together in a real DevOps workflow.

## The Problem

Manual deployments are slow and error-prone — and skipping security checks before deployment is a common way vulnerabilities reach production. This project explores building a pipeline that automates both the deployment and a basic security check before code goes live.

## What This Pipeline Does

Triggers automatically on every push to main
Runs a basic lint/test step on the code
Runs a simple security check (e.g. scanning for hardcoded AWS credentials in the code)
Deploys the application to AWS if all checks pass

## How It Works
Defined in .github/workflows/deploy.yml using GitHub Actions:
Build stage — installs dependencies, runs tests
Security stage — scans for secrets/hardcoded credentials before deployment is allowed
Deploy stage — uses AWS CLI/boto3 to push the application to AWS (e.g. S3 static hosting or EC2)

## What I Learned

This project taught me how CI/CD pipelines work end-to-end, and specifically how a security check can be built directly into a deployment pipeline rather than treated as a separate, later step — the "shift-left" security idea I'd only read about before building this.
Status
Early-stage learning project — currently deploys a simple static site to S3; next step is adding more thorough security scanning (dependency vulnerability checks).

## Tech Used

Python, AWS, Docker, GitHub Actions, CI/CD

## Author 

Vishal Ranjan 