# import flask libs
from flask_restful import Resource, reqparse
from constants import constants
#from flask_jwt import jwt_required

# import model
from models.customers import CustomerModel

class Customer(Resource):
    # adds a parser to handle PUT HTTP requests
    parser = reqparse.RequestParser()
    parser.add_argument('name',type=str,required=False)
    parser.add_argument('email',type=str,required=False)
    parser.add_argument('birth_date',type=str,required=False)

    # TODO: to handle HTTP GET /raw_material?id=?<int:id>
    def get(self, id):
        customer = CustomerModel.find_by_id(id)
        if customer:
            return customer.json(), 200
        else:
            return {'Message': constants['ID_NOT_EXIST']}

    def delete(self, id):
        # checks if material exists in database
        customer = CustomerModel.find_by_id(id)

        # in case it exists, delete it
        if customer:
            customer.delete_from_db()
            
        # return message and default HTTP status (200 - OK)
        return {'Message': constants['DELETED']}

    def put(self, id):
        # gets parameter from parser
        data = Customer.parser.parse_args()

        # checks if material exists in database
        customer = CustomerModel.find_by_id(id)

        # in case it exists, updates it
        if customer:
            for key in data.keys():
                if key=='name' and data['name']:
                        customer.name = data['name']
                if key=='email' and data['email']:
                        customer.email = data['email']
                if key=='birth_date' and data['birth_date']:
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

class Customers(Resource):
    # adds a parser to handle POST HTTP requests
    parser = reqparse.RequestParser()
    parser.add_argument('name',type=str,required=True)
    parser.add_argument('email',type=str,required=False)
    parser.add_argument('birth_date',type=str,required=False)

    # handles HTTP request GET /customers
    def get(self):
        return [x.json() for x in CustomerModel.query.all()]

    # handles HTTP request POST /customers
    def post(self):
        # gets parameter from parser
        data = Customers.parser.parse_args()

        # checks if material exists in database
        customer = CustomerModel.find_by_name(data['name'])

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

# class used to get the orders from customer
class OrderList(Resource):
    # route: customer/<int:id>/orders
    def get(self, id):
        customer = CustomerModel.find_by_id(id)
        if customer:
            return customer.get_orders_from_customer()
        else:
            return {'message' : constants['ID_NOT_FOUND']}