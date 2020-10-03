# import flask libs
from flask_restful import Resource, reqparse
from flask import request
from datetime import datetime
#from flask_jwt import jwt_required

from models.orders import OrderModel

class Order(Resource):

    # adds a parser to handle POST HTTP requests
    parser = reqparse.RequestParser();
    parser.add_argument('product_id',type=int,required=True);
    parser.add_argument('customer_id',type=int,required=True);
    parser.add_argument('notes',type=str,required=False);

    # TODO: to handle HTTP GET /order?id=?<int:id>
    def get(self):
        id_ = request.args.get('id')
        order = OrderModel.find_by_id(id_)
        return order.json(), 200

    def post(self):
        # gets parameter from parser
        data = Order.parser.parse_args()
        
        # creates a new order
        order = OrderModel(**data)

        # tries to insert in database, returns 500 (internal server error) in case of database failure
        try:
            order.save_to_db()
        except:
            return {"message": "An error occurred upon inserting the into the database."}, 500

        # returns JSON with the created Material and returns CREATED status (201)
        return order.json(), 201

    def delete(self):
        # checks if material exists in database
        id_ = request.args.get('id')
        order = OrderModel.find_by_id(id_)

        # in case it exists, delete it
        if order:
            order.delete_from_db()
            
        # return message and default HTTP status (200 - OK)
        return {'Message': 'Order has been deleted'}

# class used to get the whole list of materials in the database
# request GET /orders
class OrderList(Resource):
    def get(self):
        return {'orders': [x.json() for x in OrderModel.query.all()]}
