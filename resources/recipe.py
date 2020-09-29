# import flask libs
from flask_restful import Resource, reqparse
from flask import request
#from flask_jwt import jwt_required

from datetime import datetime
from constants import constants

# import model
from models.recipe import RecipeModel

class Recipe(Resource):

    # adds a parser to handle PUT an POST HTTP requests
    parser = reqparse.RequestParser()
    parser.add_argument('description',type=str,required=False)
    parser.add_argument('labor_cost',type=float,required=False)
    parser.add_argument('supply_cost',type=float,required=False)

    # to handle HTTP GET /recipe?id=<int:id>
    def get(self):
        id_ = request.args.get('id')
        recipe = RecipeModel.find_by_id(id_)
        return recipe.json(), 200

    def post(self):
        # gets parameter from parser
        data = Recipe.parser.parse_args()

        # checks if material exists in database
        id_ = request.args.get('id')
        recipe = RecipeModel.find_by_id(id_)

        # in case it exists, returns a message and HTTP 400 code (BAD REQUEST)
        if recipe:
            return {'message': constants['ITEM_EXISTS'].format(description)}, 400

        # in case it does not exist, creates a new recipe using data passed
        # along with the HTTP request
        recipe = RecipeModel(**data)

        # tries to insert in database
        # returns 500 (internal server error) in case of database failure
        try:
            recipe.save_to_db()
        except:
            return {"message": constants['INSERT_FAIL']}, 500

        # returns JSON with the created Material and returns CREATED status (201)
        return recipe.json(), 201

    def delete(self):
        # checks if material exists in database
        id_ = request.args.get('id')
        recipe = RecipeModel.find_by_id(id_)

        # in case it exists, delete it
        if recipe:
            recipe.delete_from_db()

        # return message and default HTTP status (200 - OK)
        return {'message': constants['DELETED'].format(description)}

    def put(self):
        # gets parameter from parser
        data = Recipe.parser.parse_args()

        # checks if item exists in database
        id_ = request.args.get('id')
        recipe = RecipeModel.find_by_id(id_)

        # in case it exists, updates it
        if recipe:
            for key in data.keys():
                if key=='description':
                    recipe.description = data['description']
                if key=='labor_cost':
                    recipe.labor_cost = data['labor_cost']
                if key=='supply_cost':
                    recipe.supply_cost = data['supply_cost']
                if key=='sell_by_date':
                    recipe.sell_by_date = data['sell_by_date']
                if key=='materials':
                    pass
            recipe.last_update = datetime.now().strftime("%d/%m/%Y %H:%M")

        # in case not exist, creates a new item
        else:
            recipe = RecipeModel(**data)

        # tries to insert in database
        # returns 500 (internal server error) in case of database failure
        try:
            recipe.save_to_db()
        except:
            return {"message": constants['INSERT_FAIL']}, 500

        # returns
        return recipe.json()


# class used to get the whole list of recipes from the database
class RecipeList(Resource):
    def get(self):
        return {'Recipes': [x.json() for x in RecipeModel.query.all()]}

# class used to get the whole list of materials in a recipe
class MaterialList(Resource):
    # route: recipe/<int:recipe_id>
    def get(self, recipe_id):

        recipe = RecipeModel.find_by_id(recipe_id)

        if recipe:
            return {'Materials': [x.json() for x in recipe.get_all_materials()]}
        else:
            return {'message' : constants['ID_NOT_FOUND']}
