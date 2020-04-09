# import flask libs
from flask_restful import Resource, reqparse
#from flask_jwt import jwt_required

# import model
from models.raw_material import RawMaterialModel

class RawMaterial(Resource):

    # adds a parser to handle PUT an POST HTTP requests
    parser_create = reqparse.RequestParser()
    parser_create.add_argument('description',type=str,required=True,help="This field cannot be left blank!")
    parser_create.add_argument('package_price',type=float,required=True,help="This field cannot be left blank!")
    parser_create.add_argument('package_amt',type=int,required=True,help="This field cannot be left blank!")
    parser_create.add_argument('unit_material',type=str,required=True,help="This field cannot be left blank!")
    parser_create.add_argument('stock_amt',type=int,required=False)
    parser_create.add_argument('sell_by_date',type=str,required=False)

    # adds a parser to handle DEL HTTP requests
    parser_delete = reqparse.RequestParser()
    parser_delete.add_argument('description',type=str,required=True,help="This field cannot be left blank!")

    # TODO: to handle HTTP GET /raw_material/<string:part_number>
    def get(self, part_number):
        pass

    def post(self):
        # gets parameter from parser
        data = RawMaterial.parser_create.parse_args()

        # checks if material exists in database
        description = data['description']
        raw_material = RawMaterialModel.find_by_name(description)

        # in case it exists, returns a message and HTTP 400 code (BAD REQUEST)
        if raw_material:
            return {'message': "A raw material with descripton '{}' already exists.".format(description)}, 400

        # in case it does not exist, creates a new material using data passed
        # along with the HTTP request
        raw_material = RawMaterialModel(**data)

        # tries to insert in database
        # returns 500 (internal server error) in case of database failure
        try:
            raw_material.save_to_db()
        except:
            return {"message": "An error occurred upon inserting the into the database."}, 500

        # returns JSON with the created Material and returns CREATED status (201)
        return raw_material.json(), 201

    def delete(self):
        # gets parameter from parser
        data = RawMaterial.parser_delete.parse_args()
        description = data['description']

        # checks if material exists in database
        raw_material = RawMaterialModel.find_by_name(description)

        # in case it exists, delete it
        if raw_material:
            raw_material.delete_from_db()
            
        # return message and default HTTP status (200 - OK)
        return {'message': 'Item deleted'}

    def put(self):
        # gets parameter from parser
        data = RawMaterial.parser_create.parse_args()

        # checks if material exists in database
        description = data['description']
        raw_material = RawMaterialModel.find_by_name(description)

        # in case it exists, updates it
        if raw_material:
            raw_material.package_price = data['package_price']
            raw_material.package_amt = data['package_amt']
            raw_material.unit_material = data['unit_material']
            raw_material.stock_amt = data['stock_amt']
            raw_material.sell_by_date = data['sell_by_date']

        # in case it does not exist, creates a new material using data passed
        # along with the HTTP request
        else:
            raw_material = RawMaterialModel(**data)

        # tries to insert in database
        # returns 500 (internal server error) in case of database failure
        try:
            raw_material.save_to_db()
        except:
            return {"message": "An error occurred with the database."}, 500

        # returns
        return raw_material.json()

# class used to get the whole list of materials in the database
# route: /raw_materials
class RawMaterialList(Resource):
    def get(self):
        return {'Raw Materials': [x.json() for x in RawMaterialModel.query.all()]}
