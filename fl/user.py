import auth
import location_repository

class User:
    def __init__(self, db, id=None, username=None, password=None):
        self.id = id
        self.username = username
        self.password = password
        self._db = db

    def create(self):
        if not self.id:
            self.id = self._db.insert("user", username=self.username, password=auth.hash(self.password))
        return self.id

    def has_location(self, location_id):
        row = self._db.fetch_one(
            """SELECT user_id, location_id
               FROM user_location
               WHERE user_id = %s AND location_id = %s""",
            (self.id, location_id)
        )
        return row is not None

    def add_location(self, location_id):
        if not self.id or self.has_location(location_id):
            return

        self.id = self._db.insert("user_location", user_id=self.id, location_id=location_id)

    def remove_location(self, location_id):
        if not self.id or not self.has_location(location_id):
            return

        self._db.delete("user_location", "user_id = " + self.id + " AND location_id = " + location_id)
        self._db.delete("location", "id = " + location_id)

    def get_locations(self):
        return location_repository.find_by_user_id(self._db, self.id)

    def to_dict(self):
        return {"id": self.id, "username": self.username}

    def update(self, username=None, password=None):
        if not self.id:
            return
        params = dict()
        if username is not None:
            params["username"] = username
        if password is not None:
            params["password"] = auth.hash(password)

        if params:
            self._db.update("user", "id = " + str(self.id), params)

