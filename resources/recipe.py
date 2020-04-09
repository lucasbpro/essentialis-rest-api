# import flask libs
from flask_restful import Resource, reqparse
#from flask_jwt import jwt_required

from datetime import datetime
from constants import constants

# import model
from models.recipe import RecipeModel

class Recipe(Resource):

    # adds a parser to handle PUT an POST HTTP requests
    parser_create = reqparse.RequestParser()
    parser_create.add_argument('description',type=str,required=True,help=constants['HELP_PARSER'])
    parser_create.add_argument('labor_cost',type=float,required=True,help=constants['HELP_PARSER'])
    parser_create.add_argument('supply_cost',type=float,required=True,help=constants['HELP_PARSER'])

    # adds a parser to handle DEL HTTP requests
    parser_delete = reqparse.RequestParser()
    parser_delete.add_argument('description',type=str,required=True,help=constants['HELP_PARSER'])

    # TODO: to handle HTTP GET /recipe/<string:recipe_code>
    def get(self, recipe_code):
        pass

    def post(self):
        # gets parameter from parser
        data = Recipe.parser_create.parse_args()

        # checks if material exists in database
        description = data['description']
        recipe = RecipeModel.find_by_description(description)

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

    def post(self, raw_material_id):
        return {'message' : "teste"}

    def delete(self):
        # gets parameter from parser
        data = Recipe.parser_delete.parse_args()
        description = data['description']

        # checks if material exists in database
        recipe = RecipeModel.find_by_description(description)

        # in case it exists, delete it
        if recipe:
            recipe.delete_from_db()

        # return message and default HTTP status (200 - OK)
        return {'message': constants['DELETED'].format(description)}

    def put(self):
        # gets parameter from parser
        data = Recipe.parser_create.parse_args()

        # checks if item exists in database
        description = data['description']
        recipe = RecipeModel.find_by_description(description)

        # in case it exists, updates the item
        if recipe:
            recipe.description = data['description']
            recipe.labor_cost = data['labor_cost']
            recipe.supply_cost = data['supply_cost']
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
