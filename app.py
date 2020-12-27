import os

from flask import Flask
from flask_restful import Api
from flask_cors import CORS
# from flask_jwt import JWT
#from security import authenticate, identity

# import resorces
from resources.raw_material import *
from resources.recipe import *
from resources.customers import *
from resources.orders import *

# creates Flask application
app = Flask(__name__)

# sets up production environment
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'rebequinha'

# creates API instance
CORS(app)
api = Api(app)


# jwt = JWT(app, authenticate, identity)  # /auth

# Sets up API endpoints
api.add_resource(RawMaterial, '/raw_materials/<int:id>')
api.add_resource(RawMaterials, '/raw_materials')

api.add_resource(Recipe,  '/recipes/<int:id>')
api.add_resource(Recipes,  '/recipes')
api.add_resource(MaterialList, '/recipe/<int:id>/materials')

api.add_resource(Customer, '/customers/<int:id>')
api.add_resource(Customers, '/customers')

api.add_resource(Order, '/orders/<int:id>')
api.add_resource(Orders, '/orders')

# api.add_resource(UserRegister, '/register')

<<<<<<< HEAD
    
if __name__ == '__main__':
=======
>>>>>>> main
    
if __name__ == '__main__':
    from db import db
    db.init_app(app)

    if app.config['DEBUG']:
        @app.before_first_request
        def create_tables():
            db.create_all()
            
    app.run(port=5000)
