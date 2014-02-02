import auth

class User:
    def __init__(self, db, id=None, username=None, password=None):
        self.id = id
        self.username = username
        self.password = password
        self._db = db

    def create(self):
        if not self.id:
            return

        self.id = self._db.insert("user", username=self.username, password=auth.hash(password))

    def get_locations(self):
        query = """SELECT l.id, l.name, l.address, l.lat, l.lng
                   FROM location l
                   INNER JOIN user_location ul ON ul.location_id = l.id
                   WHERE ul.user_id = %s"""
        rows = self._db.fetch_all(query, (self.id,))
        return ({"id": row[0], "name": row[1], "address": row[2], "lat": row[3], "lng": row[4]} for row in rows)

    def to_dict(self):
        return {"id": self.id, "username": self.username}

    def update(self, username=None, password=None):
        if self.id is None:
            return
        params = dict()
        if username is not None:
            params["username"] = username
        if password is not None:
            params["password"] = auth.hash(password)

        if params:
            self._db.update("user", "id = " + str(self.id), value_pairs)

