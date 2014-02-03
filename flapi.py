from flask import Flask, g
from flask.ext.restful import reqparse, abort, Api, Resource

import fl

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username', type=str)
_user_parser.add_argument('password', type=str)

class User(Resource):
    def get(self, user_id):
        row = fl.user_repository.find_one_by(g.db, id=user_id)
        if row is None:
            abort(404, message="User id {} can not be found.".format(user_id))

        return row, 201

class UserList(Resource):
    def post(self):
        args = _user_parser.parse_args()
        if not args["username"] or not args["password"]:
            abort(400, message="Username and password are both required")
        user = fl.user_repository.find_one_by(g.db, username=args["username"])
        if user:
            abort(400, message="Username {} has already existed".format(args["username"]))
        user = fl.User(g.db, username=args["username"], password=args["password"])
        user.create()
        return user.to_dict(), 201
    

_location_parser = reqparse.RequestParser()
_location_parser.add_argument('name', type=str)
_location_parser.add_argument('address', type=str)
_location_parser.add_argument('lat', type=float)
_location_parser.add_argument('lng', type=float)

class Location(Resource):
    def get(self, location_id):
        row = fl.location_repository.find_one_by(g.db, id=location_id)
        if row is None:
            abort(404, message="Location id {} can not be found.".format(location_id))

        return row, 201

    def put(self, location_id):
        location = fl.location_repository.find_one_by(g.db, id=location_id)
        if location is None:
            abort(404, message="Location id {} can not be found.".format(location_id))
        location = fl.Location(g.db, location_id)
        args = _location_parser.parse_args()
        location.update(**args)
        return location.to_dict(), 201

    def delete(self, location_id):
        fl.location_repository.delete_by_id(g.db, location_id)
        return {"message": "Deleted"}, 201


class LocationList(Resource):
    def get(self):
        rows = fl.location_repository.find_all(g.db);
        if rows is None:
            abort(404, message="User id {} does not have any locations.".format(location_id))

        return rows, 201    

    def post(self):
        args = _location_parser.parse_args()
        if not args["name"] or not args["lat"] or not args["lng"]:
            abort(400, message="Location name, lat, and lng are all required.")

        location = fl.Location(g.db, **args)
        location.create()
        return location.to_dict(), 201

    
class UserLocation(Resource):
    def get(self, user_id):
        rows = fl.location_repository.find_by_user_id(g.db, user_id)
        if rows is None:
            abort(404, message="User id {} does not have any locations.".format(user_id))

        return rows, 201    

    def post(self, user_id, location_id):
        ##TODO: check whether both user and location exist, otherwise 404
        user = fl.User(g.db, id=user_id)
        if not user.has_location(location_id):
            user.add_location(location_id)
        return {"message": "Added"}, 201

def init_api(app):
    api = Api(app)
    api.add_resource(UserList, "/api/users")
    api.add_resource(User, "/api/users/<string:user_id>")
    api.add_resource(LocationList, "/api/locations")
    api.add_resource(Location, "/api/locations/<string:location_id>")
    api.add_resource(UserLocation, "/api/user_locations/users/<string:user_id>/locations/<string:location_id>")
