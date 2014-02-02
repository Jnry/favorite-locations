from flask import Flask, g
import sys
import unittest

sys.path.append("/home/ec2-user/favorite-locations/")
import config
import database
import flapi
import schema

testapp = Flask(__name__)
testapp.testing = True
testdb = database.MySQL()
@testapp.before_request
def before_request():
    g.db = testdb
    g.db.connect(config.test_db)

@testapp.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

class FlTestCase(unittest.TestCase):
    def setUp(self):
        self.api = flapi.init_api(testapp)
        self.app = testapp
        testdb.connect(config.test_db)
        schema.update_schema(testdb)
        testdb.close()

    def tearDown(self):
        testdb.connect(config.test_db)
        testdb.truncate_all()
        testdb.close()
