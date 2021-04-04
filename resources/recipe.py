# import flask libs
from flask_restful import Resource, reqparse
from flask import request
#from flask_jwt import jwt_required

from datetime import datetime
from constants import constants

# import model
from models.recipe import RecipeModel
from models.raw_material import RawMaterialModel 
from models.recipe_material_amt import RecipeMaterialAmountModel

class Recipe(Resource):

    # adds a parser to handle PUT an POST HTTP requests
    parser = reqparse.RequestParser()
    parser.add_argument('description',type=str,required=False)
    parser.add_argument('labor_cost',type=float,required=False)
    parser.add_argument('supply_cost',type=float,required=False)
    parser.add_argument('materials', type=dict, action="append",required=False)

    # to handle HTTP GET /recipes/<int:id>
    def get(self, id):
        recipe = RecipeModel.find_by_id(id)
        if recipe:
            return recipe.json(), 200
        else:
            return {'message': constants['ID_NOT_FOUND']}

    def delete(self, id):
        # checks if material exists in database
        recipe = RecipeModel.find_by_id(id)

        # in case it exists, delete it
        if recipe:
            recipe.delete_from_db()

        # return message and default HTTP status (200 - OK)
        return {'message': constants['DELETED']}

    def put(self, id):
        # gets parameter from parser
        data = Recipe.parser.parse_args()

        # checks if item exists in database
        recipe = RecipeModel.find_by_id(id)

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
                    recipe.materials.clear()            
                    materialsDict =  data['materials'][0]
                    for key in materialsDict.keys():
                        materialId = int(key)
                        materialAmount = materialsDict[key]
                        material = RawMaterialModel.find_by_id(materialId)
                        # checks if material does exist in database and, if so, links it to the recipe
                        if material:
                            recipe.materials.append(material)
                            materialRecipeItem = RecipeMaterialAmountModel.find_by_map(id, materialId)
                            # in case recipe-material map already exists, then just updates it
                            if materialRecipeItem:
                                materialRecipeItem.amount = materialAmount
                            # otherwise, create a new recipe-material map
                            else:
                                materialRecipeItem = RecipeMaterialAmountModel(id, materialId, materialAmount)
                            materialRecipeItem.save_to_db()
                        # in case any materialId provided does not exist
                        else:
                            return {"message": constants['MATERIAL_NOT_EXIST'].format(materialId)}, 400

            recipe.last_update = datetime.now().strftime("%d/%m/%Y %H:%M")

        # in case not exist, creates a new item
        else:
            recipe = RecipeModel(data['description'],data['labor_cost'],data['supply_cost'])
            materialsDict =  data['materials'][0]
            for key in materialsDict.keys():
                materialId = int(key)
                materialAmount = materialsDict[key]
                material = RawMaterialModel.find_by_id(materialId)
                if material:
                    recipe.materials.append(material)
                    materialRecipeItem = RecipeMaterialAmountModel.find_by_map(id, materialId)
                    # in case recipe-material map already exists, then just updates it
                    if materialRecipeItem:
                        materialRecipeItem.amount = materialAmount
                        materialRecipeItem.save_to_db()
                        # otherwise, create a new recipe-material map
                    else:
                        materialRecipeItem = RecipeMaterialAmountModel(id, materialId, materialAmount)
                        materialRecipeItem.save_to_db()

        # tries to insert in database
        # returns 500 (internal server error) in case of database failure
        try:
            recipe.save_to_db()
        except:
            return {"message": constants['INSERT_FAIL']}, 500

        # returns
        return recipe.json()


class Recipes(Resource):
    # adds a parser to handle POST HTTP requests
    parser = reqparse.RequestParser()
    parser.add_argument('description',type=str,required=True)
    parser.add_argument('labor_cost',type=float,required=False)
    parser.add_argument('supply_cost',type=float,required=False)
    parser.add_argument('materials',type=dict,action="append",required=True)

    # handles HTTP request GET /recipes
    def get(self):
        return [x.json() for x in RecipeModel.query.all()]

    # handles HTTP request POST /recipes
    def post(self):
        # gets parameter from parser
        data = Recipes.parser.parse_args()

        # checks if material exists in database
        recipe = RecipeModel.find_by_description(data['description'])

        # in case it exists, returns a message and HTTP 400 code (BAD REQUEST)
        if recipe:
            return {'message': constants['ITEM_EXISTS'].format(data['description'])}, 400

        # in case it does not exist, creates a new recipe using data passed
        # along with the HTTP request
        recipe = RecipeModel(data['description'],data['labor_cost'],data['supply_cost'])
        materialsDict =  data['materials'][0]
        for key in materialsDict.keys():
            materialId = int(key)
            materialAmount = materialsDict[key]
            material = RawMaterialModel.find_by_id(materialId)
            if material:
                recipe.materials.append(material)
                materialRecipeItem = RecipeMaterialAmountModel.find_by_map(recipe.id, materialId)
                # in case recipe-material map already exists, then just updates it
                if materialRecipeItem:
                    materialRecipeItem.amount = materialAmount
                    materialRecipeItem.save_to_db()
                # otherwise, create a new recipe-material map
                else:
                    materialRecipeItem = RecipeMaterialAmountModel(recipe.id, materialId, materialAmount)
                    materialRecipeItem.save_to_db()
            # in case any materialId provided does not exist
            else:
                return {"message": constants['MATERIAL_NOT_EXIST'].format(materialId)}, 200

        # tries to insert in database
        # returns 500 (internal server error) in case of database failure
        try:
            recipe.save_to_db()
        except:
            return {"message": constants['INSERT_FAIL']}, 500

        # returns JSON with the created Material and returns CREATED status (201)
        return recipe.json(), 201

# class used to get the whole list of materials in a recipe
class MaterialList(Resource):
    # route: recipe/<int:id>/materials
    def get(self, id):
        recipe = RecipeModel.find_by_id(id)
        if recipe:
            return recipe.get_materials_amount()
        else:
            return {'message' : constants['ID_NOT_FOUND']}