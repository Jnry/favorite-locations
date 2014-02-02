import ConfigParser
import MySQLdb

class MySQL:
    def __init__(self):
        config = ConfigParser.RawConfigParser()
        config.read('../fldb/password.cfg')
        self._username = config.get('Mysql', 'username')
        self._password = config.get('Mysql', 'password')
        self._conn = None;
        self._cursor = None;

    def connect(self, db):
        self._conn = MySQLdb.connect(passwd=self._password, user=self._username, db=db)
        self._conn.autocommit(True)
        self._cursor = self._conn.cursor();

    def insert(self, table, **value_pairs):
        ## TODO: escape values and table
        key_str = ", ".join(["`" + k + "`" for k in value_pairs.iterkeys()])
        value_str = ", ".join(["'" + str(v) + "'" for v in value_pairs.itervalues()])
        
        query = "INSERT INTO " + table + " (" + key_str + ") VALUES (" + value_str + ")"
        
        self._cursor.execute(query)
        return self._conn.insert_id()

    def update(self, table, condition_str, **value_pairs):
        changes = ", ".join(["`" + k + "` = '" + str(v) + "'" for (k, v) in value_pairs.iteritems()])
        query = "UPDATE " + table + " SET " + changes
        if condition_str:
            query = query + " WHERE " + condition_str

        self._cursor.execute(query)

    def fetch_all(self, query, args=None):
        self._cursor.execute(query, args)
        return self._cursor.fetchall()

    def fetch_one(self, query, args=None):
        self._cursor.execute(query, args)
        return self._cursor.fetchone()

    def query(self, query_str):
        self._cursor.execute(query_str)

    def close(self):
        self._conn.close()
