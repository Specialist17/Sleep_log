from flask import Flask, request, make_response
from flask_restful import Resource, Api
from pymongo import MongoClient
from utils.mongo_json_encoder import JSONEncoder
import bcrypt
from bson.json_util import dumps
import json
import pdb
# import User


app = Flask(__name__)
# app.config.from_pyfile('config.cfg')
mongo = MongoClient('localhost', 27017)
app.db = mongo.sleep_log
app.bcrypt_rounds = 12
api = Api(app)


def auth_validation(email, user_password):
    # Find user by email
    user_col = app.db.users
    database_user = user_col.find_one({'email': email})
    if database_user is None:
        return({"error": "email not found"}, 404, None)
    db_password = database_user.get('password')
    user_id = database_user["_id"]

    password = user_password.encode('utf-8')
    # pdb.set_trace()
    # Check if client password from login matches database password
    if bcrypt.hashpw(password, db_password) == db_password:
        # Let them in
        return (user_id, 200, None)
    return (None, 400, None)


def auth_function(func):
    def wrapper(*args, **kwargs):
        auth = request.authorization
        print(auth)
        validation = auth_validation(auth.username, auth.password)
        if validation[1] is 400:
            return (
                    'Could not verify your access level for that URL.\n'
                    'You have to login with proper credentials', 401,
                    {'Authentication': 'Basic base64"'}
                   )
        else:
            return func(*args, validation[0], **kwargs)
    return wrapper


# Write Resources here
class User(Resource):

    def post(self):
        pass

    @auth_function
    def get(self, user_id):
        pass

    @auth_function
    def put(self, user_id):
        pass

    @auth_function
    def delete(self, user_id):
        pass


class Logs(Resource):

    @auth_function
    def get(self, user_id):
        pass

    @auth_function
    def post(self, user_id):
        pass

    @auth_function
    def put(self, user_id):
        pass

    @auth_function
    def delete(self, id):
        pass


# Add api routes here
api.add_resource(User, '/users')
api.add_resource(Trip, '/trips')


#  Custom JSON serializer for flask_restful
@api.representation('application/json')
def output_json(data, code, headers=None):
    resp = make_response(JSONEncoder().encode(data), code)
    resp.headers.extend(headers or {})
    return resp


if __name__ == '__main__':
    # Turn this on in debug mode to get detailled information about request
    # related exceptions: http://flask.pocoo.org/docs/0.10/config/
    app.config['TRAP_BAD_REQUEST_ERRORS'] = True
    app.run()
