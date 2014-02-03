from flask import g
import sys
import unittest

sys.path.append("/home/ec2-user/favorite-locations/")
import fl
import testing

class TestFlapi(testing.FlTestCase):
    def test_add_user(self):
        with self.app.test_client() as client:
            user_data = self._generate_user_data()
            response = client.post(path="/api/users", data=user_data)
            self.assertEqual(response.status_code, 201)

            response = client.post(path="/api/users", data=user_data)
            self.assertEqual(response.status_code, 400)
        
    def test_add_location(self):
        with self.app.test_client() as client:
            response = client.post(path="/api/locations", data=self._generate_location_data())
            self.assertEqual(response.status_code, 201)
            
            response = client.post(path="/api/locations", data={"name": "test"})
            self.assertEqual(response.status_code, 400)
            print response.headers

    def test_connect_user_location(self):
        location = fl.Location(self.db, **self._generate_location_data())
        lid = location.create()
        user = fl.User(self.db, **self._generate_user_data())
        uid = user.create()

        with self.app.test_client() as client:
            response = client.post(path="/api/user_locations/users/%s/locations/%s" % (uid, lid))
            self.assertEqual(response.status_code, 201)

    def _generate_user_data(self):
        return {"username": "test2", "password": "123"}

    def _generate_location_data(self):
        return {"name": "test", "address": "xxx", "lat": 123.2, "lng": 234.3}

    
if __name__ == "__main__":
    unittest.main()
