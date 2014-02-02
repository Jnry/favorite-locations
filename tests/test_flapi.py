import unittest

import testing

class TestFlapi(testing.FlTestCase):
    def test_add_user(self):
        client = self.app.test_client()
        response = client.post(path="/users", data={"username": "test2", "password": "123"})

        
if __name__ == "__main__":
    unittest.main()
