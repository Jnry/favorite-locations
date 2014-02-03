import location_repository

class Location:
    def __init__(self, db, id=None, name=None, address=None, lat=None, lng=None):
        self.id = id
        self.name = name
        self.address = address
        self.lat = lat
        self.lng = lng
        self._db = db

    def create(self):
        if not self.id:
            self.id = self._db.insert("location", name=self.name, address=self.address, lat=self.lat, lng=self.lng)
        return self.id

    def to_dict(self):
        return location_repository.find_one_by(self._db, id=self.id)

    def update(self, name=None, address=None, lat=None, lng=None):
        if not self.id:
            return
        params = dict()
        if name is not None:
            params["name"] = name
        if address is not None:
            params["address"] = address
        if lat is not None:
            params["lat"] = lat
        if lng is not None:
            params["lng"] = lng

        if params:
            self._db.update("location", "id = " + str(self.id), **params)
