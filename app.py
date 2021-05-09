import os

from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_jwt import JWT
from security import authenticate, identity

# import resorces
from resources.raw_material import *
from resources.recipe import *
from resources.product import *
from resources.customers import *
from resources.orders import *
from resources.recipe_material_amt import *
from resources.users import *

# creates Flask application
app = Flask(__name__)

# sets up LOCAL environment
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'   # local db file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'rebequinha'

# creates API instance
CORS(app)
api = Api(app)

# creates jwt functionality for user authentication (/auth)
jwt = JWT(app, authenticate, identity)

# Sets up API endpoints
api.add_resource(Users, '/users')

api.add_resource(RawMaterial, '/raw_materials/<int:id>')
api.add_resource(RawMaterials, '/raw_materials')

api.add_resource(Recipe,  '/recipes/<int:id>')
api.add_resource(Recipes,  '/recipes')
api.add_resource(MaterialList, '/recipe/<int:id>/materials')
api.add_resource(RecipeMaterialAmount,'/recipe/<int:recipe_id>/material/<int:material_id>')

api.add_resource(Product, '/products/<int:id>')
api.add_resource(Products, '/products')

api.add_resource(Customer, '/customers/<int:id>')
api.add_resource(Customers, '/customers')

api.add_resource(Order, '/orders/<int:id>')
api.add_resource(Orders, '/orders')
api.add_resource(OrderList, '/customers/<int:id>/orders')

# api.add_resource(UserRegister, '/register')
    
if __name__ == '__main__':
    from db import db
    db.init_app(app)

    if app.config['DEBUG']:
        @app.before_first_request
        def create_tables():
            db.create_all()
            
            # creates an admin user before initializing the app
            from models.user import UserModel
            adminUser = UserModel.find_by_username("admin")
            if adminUser:
                pass
            else: 
                adminUser = UserModel("admin",os.environ.get('ADMIN_PASSWORD', 'testeAdmin'))
                adminUser.save_to_db()

    app.run(port=5000)


