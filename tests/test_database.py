import sys
import unittest
sys.path.append('/home/ec2-user/favorite-locations/')
import database
import config

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.db = database.MySQL()
        self.db.connect(config.test_db)
        self.db.query("CREATE TABLE test (id int primary key auto_increment, name varchar(255) not null)")

    def test_insert(self):
        id = self.db.insert("test", name="test")
        self.assertEqual(id, 1)

        id = self.db.insert("test", name="test2")
        self.assertEqual(id, 2)

    def test_update(self):
        id = self.db.insert("test", name="test")
        self.db.update("test", "id = " + str(id), name="test2")
        row = self.db.fetch_all("SELECT name FROM test WHERE id = %s", (id,))
        self.assertEqual(row, (("test2",),))

    def test_fetch_all(self):
        self.db.insert("test", name="test1")
        self.db.insert("test", name="test2")
        rows = self.db.fetch_all("SELECT name FROM test")
        self.assertEqual(rows, (("test1",), ("test2",),))

        row = self.db.fetch_all("SELECT name FROM test WHERE id > %s", (1,))
        self.assertEqual(row, (("test2",),))

    def test_fetch_one(self):
        self.db.insert("test", name="test1")
        v = self.db.fetch_one("SELECT name FROM test")
        self.assertEqual(v, ("test1",))

    def tearDown(self):
        self.db.query("DROP TABLE IF EXISTS test")
        self.db.close()

if __name__ == "__main__":
    unittest.main()
