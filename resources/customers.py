# import flask libs
from flask_restful import Resource, reqparse
from flask import request
#from flask_jwt import jwt_required

# import model
from models.customers import CustomerModel

class Customer(Resource):

    # adds a parser to handle PUT an POST HTTP requests
    parser = reqparse.RequestParser()
    parser.add_argument('name',type=str,required=False)
    parser.add_argument('email',type=str,required=False)
    parser.add_argument('birth_date',type=str,required=False)

    # TODO: to handle HTTP GET /raw_material?id=?<int:id>
    def get(self):
        id_ = request.args.get('id')
        customer = CustomerModel.find_by_id(id_)
        return customer.json(), 200

    def post(self):
        # gets parameter from parser
        data = Customer.parser.parse_args()

        # checks if material exists in database
        id_ = request.args.get('id')
        customer = CustomerModel.find_by_id(id_)

        # in case it exists, returns a message and HTTP 400 code (BAD REQUEST)
        if customer:
            return {'message': "A customer with name '{}' already exists.".format(data['name'])}, 400

        # in case it does not exist, creates a new material using data passed
        # along with the HTTP request
        customer = CustomerModel(**data)

        # tries to insert in database
        # returns 500 (internal server error) in case of database failure
        try:
            customer.save_to_db()
        except:
            return {"message": "An error occurred upon inserting the into the database."}, 500

        # returns JSON with the created Material and returns CREATED status (201)
        return customer.json(), 201

    def delete(self):
        # checks if material exists in database
        id_ = request.args.get('id')
        customer = CustomerModel.find_by_id(id_)

        # in case it exists, delete it
        if customer:
            customer.delete_from_db()
            
        # return message and default HTTP status (200 - OK)
        return {'Message': 'Customer has been deleted'}

    def put(self):
        # gets parameter from parser
        data = Customer.parser.parse_args()

        # checks if material exists in database
        id_ = request.args.get('id')
        customer = CustomerModel.find_by_id(id_)

        # in case it exists, updates it
        if customer:
            for key in data.keys():
                if key=='name':
                        customer.name = data['name']
                if key=='email':
                        customer.email = data['email']
                if key=='birth_date':
                        customer.birth_date = data['birth_date']

        # in case it does not exist, creates a new material using data passed
        # along with the HTTP request
        else:
            customer = CustomerModel(**data)

        # tries to insert in database
        # returns 500 (internal server error) in case of database failure
        try:
            customer.save_to_db()
        except:
            return {"message": "An error occurred with the database."}, 500

        # returns
        return customer.json()

# class used to get the whole list of materials in the database
# route: /customers
class CustomerList(Resource):
    def get(self):
        return {'Customers': [x.json() for x in CustomerModel.query.all()]}
