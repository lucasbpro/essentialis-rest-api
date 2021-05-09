# import flask libs
from flask_restful import Resource, reqparse
from constants import constants
from datetime import datetime

# import model
from models.product import ProductModel
from models.recipe import RecipeModel

class Product(Resource):
    # adds a parser to handle PUT HTTP requests
    parser = reqparse.RequestParser()
    parser.add_argument('recipe_id',type=int,required=False)
    parser.add_argument('stock_amt',type=int,required=False)

    # to handle HTTP GET /product/<int:id>
    def get(self, id):
        product = ProductModel.find_by_id(id)
        if product:
            return product.json(), 200
        else:
            return {'Message': constants['ID_NOT_FOUND']}

    # to handle HTTP DEL /product/<int:id>
    def delete(self, id):
        # checks if material exists in database
        product = ProductModel.find_by_id(id)

        # in case it exists, delete it
        if product:
            product.delete_from_db()
            
        # return message and default HTTP status (200 - OK)
        return {'Message': constants['DELETED']}

    # to handle HTTP PUT /product/<int:id>
    def put(self, id):
        # gets parameter from parser
        data = Product.parser.parse_args()

        # checks if material exists in database
        product = ProductModel.find_by_id(id)

        # in case it exists, updates it
        if product:
            for key in data.keys():
                if key=='stock_amt' and data['stock_amt']:
                    product.stock_amt = data['stock_amt']
                    product.last_update = datetime.now().strftime("%d/%m/%Y %H:%M")
                if key=='recipe_id' and data['recipe_id']:
                    recipe = RecipeModel.find_by_id(data['recipe_id'])
                    if recipe:
                        product.recipe_id = data['recipe_id']
                        product.recipe = recipe
                        product.last_update = datetime.now().strftime("%d/%m/%Y %H:%M")

        # in case it does not exist, creates a new material using data passed
        # along with the HTTP request
        else:
            product = ProductModel(**data)

        # tries to insert in database, returns 500 (internal server error) in case of database failure
        try:
            product.save_to_db()
        except:
            return {"message": "An error occurred with the database."}, 500

        # returns
        return product.json()

class Products(Resource):
    # adds a parser to handle POST HTTP requests
    parser = reqparse.RequestParser()
    parser.add_argument('recipe_id',type=int,required=True)
    parser.add_argument('stock_amt',type=int,required=False)

    # handles HTTP request GET /products
    def get(self):
        return [x.json() for x in ProductModel.query.all()]

    # handles HTTP request POST /products
    def post(self):
        # gets parameter from parser
        data = Products.parser.parse_args()

        # checks if material exists in database
        product = ProductModel.find_by_recipe_id(data['recipe_id'])

        # in case it exists, returns a message and HTTP 400 code (BAD REQUEST)
        if product:
            return {'message': "A product related to recipe_id '{}' already exists.".format(data['recipe_id'])}, 400

        # in case it does not exist, creates a new material using data passed
        # along with the HTTP request
        product = ProductModel(data['recipe_id'], data['stock_amt'])

        # tries to insert in database
        # returns 500 (internal server error) in case of database failure
        try:
            product.save_to_db()
        except:
            return {"message": "An error occurred upon inserting the into the database."}, 500

        # returns JSON with the created Material and returns CREATED status (201)
        return product.json(), 201