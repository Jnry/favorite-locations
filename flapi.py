from flask import Flask, g
from flask.ext.restful import reqparse, abort, Api, Resource

import fl

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username', type=str)
_user_parser.add_argument('password', type=str)

class User(Resource):
    def get(self, user_id):
        row = fl.user_repository.find_by(g.db, id=user_id)
        if row is None:
            abort(404, message="User id {} can not be found.".format(user_id))

        return row

class UserList(Resource):
    def post(self):
        args = _user_parser.parse_args()
        if not args["username"] or not args["password"]:
            abort(400, message="Username and password are both required")
        user = fl.user_repository.find_by(g.db, username=args["username"])
        if user:
            abort(400, message="Username {} has already existed".format(args["username"]))
        user = fl.User(username=args["username"], password=args["password"])
        user.create()
        return user.to_dict(), 201
    

_location_parser = reqparse.RequestParser()
_location_parser.add_argument('name', type=str)
_location_parser.add_argument('address', type=str)
_location_parser.add_argument('lat', type=float)
_location_parser.add_argument('lng', type=float)

class Location(Resource):
    def get(self, location_id):
        pass

class LocationList(Resource):
    def get(self):
        pass

    def post(self):
        args = _location_parser.parse_args()

class UserLocation(Resource):
    def post(self):
        pass

def init_api(app):
    api = Api(app)
    api.add_resource(UserList, "/users")
    api.add_resource(User, "/users/<string:user_id>")
    api.add_resource(LocationList, "/users/<string:user_id>/locations")
    api.add_resource(Location, "/users/<string:user_id>/locations/<string:location_id>")
    api.add_resource(UserLocation, "/users/<string:user_id>/connect/add_locations/<string:location_id>")
