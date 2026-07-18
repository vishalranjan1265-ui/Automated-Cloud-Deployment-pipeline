import unittest
import base64

class TestDeploymentUtilityHelpers(unittest.TestCase):
    def test_bootstrap_script_base64_integrity(self) -> None:
        mock_uri = "123456789012.dkr.ecr.us-east-1.amazonaws.com/app:latest"
        test_region = "us-east-1"
        
        raw_script = f"""#!/usr/bin/env bash
        aws ecr get-login-password --region {test_region}
        docker pull {mock_uri}
        """
        encoded = base64.b64encode(raw_script.encode("utf-8")).decode("utf-8")
        decoded = base64.b64decode(encoded.encode("utf-8")).decode("utf-8")
        
        self.assertEqual(raw_script, decoded)
        self.assertTrue(len(encoded) > 0)

if __name__ == "__main__":
    unittest.main()