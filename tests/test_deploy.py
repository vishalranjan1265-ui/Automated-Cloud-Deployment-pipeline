import unittest
from unittest.mock import MagicMock, patch
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

with patch.dict(os.environ, {"ECR_IMAGE_URI": "123456789012.dkr.ecr.us-east-1.amazonaws.com/test-repo:latest"}):
    from deploy import CloudDeploymentOrchestrator

class TestDeploymentOrchestrator(unittest.TestCase):
    @patch("boto3.client")
    def test_resolve_network_targets_success(self, mock_boto_client: MagicMock) -> None:
        mock_ec2 = MagicMock()
        mock_boto_client.return_value = mock_ec2
        
        mock_ec2.describe_vpcs.return_value = {"Vpcs": [{"VpcId": "vpc-test1234"}]}
        mock_ec2.describe_subnets.return_value = {"Subnets": [{"SubnetId": "subnet-test1234"}]}
        
        orchestrator = CloudDeploymentOrchestrator()
        vpc_id, subnet_id = orchestrator.resolve_default_vpc_and_subnet()
        
        self.assertEqual(vpc_id, "vpc-test1234")
        self.assertEqual(subnet_id, "subnet-test1234")

    @patch("boto3.client")
    def test_provision_security_group_reuse_logic(self, mock_boto_client: MagicMock) -> None:
        mock_ec2 = MagicMock()
        mock_boto_client.return_value = mock_ec2
        
        mock_ec2.describe_security_groups.return_value = {
            "SecurityGroups": [{"GroupId": "sg-preset1234"}]
        }
        
        orchestrator = CloudDeploymentOrchestrator()
        sg_id = orchestrator.provision_security_group("vpc-test1234")
        
        self.assertEqual(sg_id, "sg-preset1234")
        mock_ec2.create_security_group.assert_not_called()

if __name__ == "__main__":
    unittest.main()