from flask import Flask, g
import sys
import unittest

sys.path.append("/home/ec2-user/favorite-locations/")
import config
import database
import flapi
import schema

_testapp = Flask(__name__)
_testapp.testing = True
_api = flapi.init_api(_testapp)

@_testapp.before_request
def before_request():
    g.db = database.MySQL()
    g.db.connect(config.test_db)

@_testapp.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()
        

class FlTestCase(unittest.TestCase):
    def setUp(self):
        self.app = _testapp
        self.db = database.MySQL()
        self.db.connect(config.test_db)
        schema.update_schema(self.db)

    def tearDown(self):
        self.db.truncate_all()
        self.db.close()
