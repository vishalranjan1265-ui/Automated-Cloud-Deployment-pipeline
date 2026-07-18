import json
import unittest
from app import app

class TestAppEngine(unittest.TestCase):
    def setUp(self) -> None:
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()

    def tearDown(self) -> None:
        self.ctx.pop()

    def test_index_route_schema(self) -> None:
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data.decode("utf-8"))
        self.assertEqual(data["status"], "OPERATIONAL")
        self.assertIn("application", data)
        self.assertIn("hostname", data)

    def test_health_check_probe(self) -> None:
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data.decode("utf-8"))
        self.assertEqual(data["status"], "UP")
        self.assertIn("container_id", data)

if __name__ == "__main__":
    unittest.main()