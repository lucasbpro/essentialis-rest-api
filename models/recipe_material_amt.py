
from db import db 
from constants import constants   # constants dictionary
from datetime import datetime

# defines the model for 'recipe_material_amt' table in db
class RecipeMaterialAmountModel(db.Model):

    # name of the table in database
    __tablename__ = 'recipe_material_amt'

    # define columns in table
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer)
    material_id = db.Column(db.Integer)
    amount = db.Column(db.Float)
    creation_date = db.Column(db.String(constants['MEDIUM_LENGTH']))
    last_update = db.Column(db.String(constants['MEDIUM_LENGTH']))

    def __init__(self, recipe_id, material_id, amount):
        self.recipe_id = recipe_id
        self.material_id = material_id 
        self.amount = amount
        self.creation_date = datetime.now().strftime("%d/%m/%Y %H:%M")
        self.last_update = self.creation_date

    def json(self):
        return  {'id'           : self.id,
                 'recipe_id'    : self.recipe_id,
                 'material_id'  : self.material_id,
                 'amount'       : self.amount,
                 'creation_date': self.creation_date,
                 'last_update'  : self.last_update,
                 }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_map(cls, recipe_id, material_id):
        return cls.query.filter_by(recipe_id=recipe_id).filter_by(material_id=material_id).first()

    @classmethod
    def find_by_recipe_id(cls, id):
        return cls.query.filter_by(recipe_id=id).first()

    @classmethod
    def find_by_material_id(cls, id):
        return cls.query.filter_by(material_id=id).first()
