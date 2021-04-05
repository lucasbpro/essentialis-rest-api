# import model

from flask_restful import Resource

from models.user import UserModel

class Users(Resource):

    # handles HTTP GET /users
    def get(self):
        return [x.json() for x in UserModel.query.all()]