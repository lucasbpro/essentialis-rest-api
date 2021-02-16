# import flask libs
from flask_restful import Resource, reqparse
from constants import constants
from datetime import datetime
#from flask_jwt import jwt_required

# import model
from models.recipe_material_amt import RecipeMaterialAmountModel

class RecipeMaterialAmount(Resource):

    # adds a parser to handle PUT HTTP requests
    parser = reqparse.RequestParser()
    parser.add_argument('amount',type=float,required=True)

    # handles HTTP PUT /recipe/<int:recipe_id>/material/<int:material_id>
    def put(self, recipe_id, material_id):
        # gets parameter from parser
        data = RecipeMaterialAmount.parser.parse_args()

        # checks if material exists in database
        recipe_material = RecipeMaterialAmountModel.find_by_map(recipe_id, material_id)

        # in case it exists, updates it
        if recipe_material:
            for key in data.keys():
                if key=='amount':
                        recipe_material.amount = data['amount']

            recipe_material.last_update = datetime.now().strftime("%d/%m/%Y %H:%M")

        # in case it does not exist, creates a new material using data passed
        # along with the HTTP request
        else:
            recipe_material = RecipeMaterialAmountModel(recipe_id, material_id, data['amount'])

        # tries to insert in database
        # returns 500 (internal server error) in case of database failure
        try:
            recipe_material.save_to_db()
        except:
            return {"message": "An error occurred with the database."}, 500

        # returns
        return recipe_material.json()

    # handles HTTP POST /recipe/<int:recipe_id>/material/<int:material_id>
    def post(self, recipe_id, material_id):
        # gets parameter from parser
        data = RecipeMaterialAmount.parser.parse_args()

        # checks if material exists in database
        recipe_material = RecipeMaterialAmountModel.find_by_map(recipe_id, material_id)

        # in case it exists, returns a message and HTTP 400 code (BAD REQUEST)
        if recipe_material:
            return {'message': "The related recipe-material map already exists."}, 400

        # in case it does not exist, creates a new material using data passed
        # along with the HTTP request
        recipe_material = RecipeMaterialAmountModel(recipe_id, material_id, data['amount'])

        # tries to insert in database
        # returns 500 (internal server error) in case of database failure
        try:
            recipe_material.save_to_db()
        except:
            return {"message": "An error occurred upon inserting the into the database."}, 500

        # returns JSON with the created Material and returns CREATED status (201)
        return recipe_material.json(), 201
