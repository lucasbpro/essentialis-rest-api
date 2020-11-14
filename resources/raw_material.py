# import flask libs
from flask_restful import Resource, reqparse
from flask import request
#from flask_jwt import jwt_required

# import model
from models.raw_material import RawMaterialModel

class RawMaterial(Resource):

    # adds a parser to handle PUT an POST HTTP requests
    parser = reqparse.RequestParser()
    parser.add_argument('description',type=str,required=False)
    parser.add_argument('package_price',type=float,required=False)
    parser.add_argument('package_amt',type=int,required=False)
    parser.add_argument('unit_material',type=str,required=False)
    parser.add_argument('stock_amt',type=int,required=False)
    parser.add_argument('sell_by_date',type=str,required=False)

    # TODO: to handle HTTP GET /raw_material?id=?<int:id>
    def get(self):
        id_ = request.args.get('id')
        raw_material = RawMaterialModel.find_by_id(id_)
        return raw_material.json(), 200

    def post(self):
        # gets parameter from parser
        data = RawMaterial.parser.parse_args()

        # checks if material exists in database
        id_ = request.args.get('id')
        raw_material = RawMaterialModel.find_by_id(id_)

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
        # checks if material exists in database
        id_ = request.args.get('id')
        raw_material = RawMaterialModel.find_by_id(id_)

        # in case it exists, delete it
        if raw_material:
            raw_material.delete_from_db()
            
        # return message and default HTTP status (200 - OK)
        return {'message': 'Item deleted'}

    def put(self):
        # gets parameter from parser
        data = RawMaterial.parser.parse_args()

        # checks if material exists in database
        id_ = request.args.get('id')
        raw_material = RawMaterialModel.find_by_id(id_)

        # in case it exists, updates it
        if raw_material:
            for key in data.keys():
                if key=='package_price':
                        raw_material.package_price = data['package_price']
                if key=='package_amt':
                        raw_material.package_amt = data['package_amt']
                if key=='unit_material':
                        raw_material.unit_material = data['unit_material']
                if key=='stock_amt':
                        raw_material.stock_amt = data['stock_amt']
                if key=='sell_by_date':
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
        return {[x.json() for x in RawMaterialModel.query.all()]}
