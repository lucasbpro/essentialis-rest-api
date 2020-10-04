import os

from flask import Flask
from flask_restful import Api
# from flask_jwt import JWT

# import other scripts
from db import db
#from security import authenticate, identity

# import resorces
from resources.raw_material import RawMaterial, RawMaterialList
from resources.recipe import *
from resources.customers import *
from resources.orders import *

# creates Flask application
app = Flask(__name__)

app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'rebequinha'

# initializes database
db.init_app(app)

# creates API instance
api = Api(app)

# jwt = JWT(app, authenticate, identity)  # /auth

# Sets up API endpoints
api.add_resource(RawMaterial, '/raw_material/<int:id>')
api.add_resource(RawMaterialList, '/raw_materials')

api.add_resource(Recipe,  '/recipe/<int:id>')
api.add_resource(RecipePost,  '/recipe')
api.add_resource(RecipeList, '/recipes')
api.add_resource(MaterialList, '/recipe/<int:id>/materials')

api.add_resource(Customer, '/customer/<int:id>')
api.add_resource(CustomerPost, '/customer')
api.add_resource(CustomerList, '/customers')

api.add_resource(Order, '/order/<int:id>')
api.add_resource(OrderPost, '/order')
api.add_resource(OrderList, '/orders')

# api.add_resource(UserRegister, '/register')


if __name__ == '__main__':
    
    if app.config['DEBUG']:
        @app.before_first_request
        def create_tables():
            db.create_all()
            
    app.run(port=5000)
