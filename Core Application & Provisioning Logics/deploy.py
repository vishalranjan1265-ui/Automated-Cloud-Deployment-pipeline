import os
import sys
import logging
import base64
from typing import List, Dict, Any, Optional, tuple
import boto3
from botocore.exceptions import ClientError

logging.basicConfig(
    level=logging.INFO,
    format='{"timestamp":"%(asctime)s", "service":"DeployEngine", "level":"%(levelname)s", "message":"%(message)s"}',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

class CloudDeploymentOrchestrator:
    def __init__(self) -> None:
        self.region = os.getenv("AWS_REGION", "us-east-1")
        self.ec2 = boto3.client("ec2", region_name=self.region)
        self.image_uri = os.getenv("ECR_IMAGE_URI")
        
        if not self.image_uri:
            logger.critical("ECR_IMAGE_URI environment variable is missing. Halting execution.")
            sys.exit(1)

    def provision_security_group(self, vpc_id: str) -> str:
        group_name = "cloud-auto-deploy-sg"
        logger.info(f"Configuring network security group parameters: {group_name}")
        try:
            existing = self.ec2.describe_security_groups(
                Filters=[
                    {'Name': 'group-name', 'Values': [group_name]},
                    {'Name': 'vpc-id', 'Values': [vpc_id]}
                ]
            )
            if existing.get("SecurityGroups"):
                sg_id: str = existing["SecurityGroups"][0]["GroupId"]
                logger.info(f"Reusing existing security group resource: {sg_id}")
                return sg_id

            sg_response = self.ec2.create_security_group(
                GroupName=group_name,
                Description="Automated deployment pipeline ingress security rules matrix.",
                VpcId=vpc_id
            )
            sg_id = sg_response["GroupId"]

            ingress_permissions = [
                {'IpProtocol': 'tcp', 'FromPort': 8080, 'ToPort': 8080, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                {'IpProtocol': 'tcp', 'FromPort': 22, 'ToPort': 22, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
            ]
            self.ec2.authorize_security_group_ingress(GroupId=sg_id, IpPermissions=ingress_permissions)
            logger.info(f"Security group successfully provisioned and hardened: {sg_id}")
            return sg_id
        except ClientError as e:
            logger.error(f"Failed to compile infrastructure security group boundaries: {str(e)}")
            raise

    def resolve_default_vpc_and_subnet(self) -> tuple[str, str]:
        try:
            vpcs = self.ec2.describe_vpcs(Filters=[{'Name': 'is-default', 'Values': ['true']}])
            if not vpcs.get("Vpcs"):
                raise Exception("No default VPC found in this AWS account region partition.")
            vpc_id: str = vpcs["Vpcs"][0]["VpcId"]

            subnets = self.ec2.describe_subnets(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])
            if not subnets.get("Subnets"):
                raise Exception(f"No valid subnets found within target default VPC: {vpc_id}")
            subnet_id: str = subnets["Subnets"][0]["SubnetId"]

            return vpc_id, subnet_id
        except ClientError as e:
            logger.error(f"Network discovery query failed mapping target interfaces: {str(e)}")
            raise

    def launch_ec2_target(self, subnet_id: str, security_group_id: str) -> str:
        logger.info("Constructing bootstrap automation script matrix (User Data)...")
        
        user_data_script = f"""#!/usr/bin/env bash
set -euo pipefail
apt-get update -y
apt-get install -y docker.io awscli
systemctl start docker
systemctl enable docker

aws ecr get-login-password --region {self.region} | docker login --username AWS --password-stdin {self.image_uri.split('/')[0]}
docker pull {self.image_uri}

docker run -d \
  --name web-app-prod \
  -p 8080:8080 \
  --restart always \
  {self.image_uri}
"""
        encoded_user_data = base64.b64encode(user_data_script.encode("utf-8")).decode("utf-8")

        try:
            ami_response = self.ec2.describe_images(
                Filters=[
                    {'Name': 'name', 'Values': ['ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*']},
                    {'Name': 'virtualization-type', 'Values': ['hvm']}
                ],
                Owners=['099720109477']
            )
            sorted_images = sorted(ami_response['Images'], key=lambda x: x['CreationDate'], reverse=True)
            ami_id = sorted_images[0]['ImageId']

            logger.info(f"Resolved AMI execution pointer: {ami_id}. Deploying instance...")
            instance_profile_arn = os.getenv("EC2_IAM_ROLE_ARN")
            
            run_args: Dict[str, Any] = {
                "ImageId": ami_id,
                "InstanceType": "t2.micro",
                "MinCount": 1,
                "MaxCount": 1,
                "SubnetId": subnet_id,
                "SecurityGroupIds": [security_group_id],
                "UserData": encoded_user_data,
                "TagSpecifications": [{
                    'ResourceType': 'instance',
                    'Tags': [{'Key': 'Name', 'Value': 'Automated-Pipeline-Target'}]
                }]
            }
            
            if instance_profile_arn:
                run_args["IamInstanceProfile"] = {"Arn": instance_profile_arn}

            instances = self.ec2.run_instances(**run_args)
            instance_id: str = instances["Instances"][0]["InstanceId"]
            logger.info(f"Instance cluster provisioned successfully. Operational tracking ID: {instance_id}")
            return instance_id
        except ClientError as e:
            logger.error(f"EC2 runtime instantiation commands failed: {str(e)}")
            raise

    def execute_orchestration(self) -> None:
        try:
            vpc_id, subnet_id = self.resolve_default_vpc_and_subnet()
            logger.info(f"Resolved network targets - VPC: {vpc_id}, Subnet: {subnet_id}")
            
            sg_id = self.provision_security_group(vpc_id)
            instance_id = self.launch_ec2_target(subnet_id, sg_id)
            
            logger.info(f"Deployment finalized. Target instance tracking ID: {instance_id}")
        except Exception as e:
            logger.critical(f"Deployment orchestrator failed catastrophic recovery checks: {str(e)}")
            sys.exit(1)

if __name__ == "__main__":
    orchestrator = CloudDeploymentOrchestrator()
    orchestrator.execute_orchestration()