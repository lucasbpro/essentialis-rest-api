# import SQLAlchemy object
from db import db
from constants import constants
from datetime import datetime

# defines the model for 'products' table in db
class ProductModel(db.Model):

    # name of the table in database
    __tablename__ = 'products'

    # define columns in table
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))
    stock_amt = db.Column(db.Integer)
    last_update = db.Column(db.String(constants['MEDIUM_LENGTH']))

    # define relationships with other tables
    recipe = db.relationship('RecipeModel')

    def __init__(self, recipe_id, stock_amt):
        self.recipe_id = recipe_id
        self.stock_amt = stock_amt or 0
        self.last_update = datetime.now().strftime("%d/%m/%Y %H:%M")

    def json(self):
        return  {
            'id'               : self.id,
            'recipe_id'        : self.recipe_id,
            'stock_amt'        : self.stock_amt,
            'last_update'      : self.last_update
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, id_):
         return cls.query.filter_by(id=id_).first()
    
    @classmethod
    def find_by_recipe_id(cls, id_):
         return cls.query.filter_by(recipe_id=id_).first()

    def get_recipe(self):
        return [self.recipe.json()]

    def get_stock_amount(self):
        return self.json().stock_amt