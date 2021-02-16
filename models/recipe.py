# import SQLAlchemy object
from db import db
from constants import constants
from datetime import datetime

# defines the model for 'recipes' table in db
class RecipeModel(db.Model):

    # name of the table in database
    __tablename__ = 'recipes'

    # define columns in table
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(constants['LONG_LENGTH']))
    labor_cost = db.Column(db.Float(constants['PRICE_PRECISION']))
    supply_cost = db.Column(db.Float(constants['PRICE_PRECISION']))
    creation_date = db.Column(db.String(constants['MEDIUM_LENGTH']))
    last_update = db.Column(db.String(constants['MEDIUM_LENGTH']))

    def __init__(self, description, labor_cost, supply_cost):
        self.description = description
        self.labor_cost = labor_cost
        self.supply_cost = supply_cost
        self.creation_date = datetime.now().strftime("%d/%m/%Y %H:%M")
        self.last_update = self.creation_date

    def json(self):
        return  {'id'               : self.id,
                 'description'      : self.description,
                 'creation_date'    : self.creation_date,
                 'last_update'      : self.last_update,
                 'labor_cost'       : self.labor_cost,
                 'supply_cost'      : self.supply_cost,
                 'materials'        : [material.id for material in self.materials]
                 }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_description(cls, description):
        return cls.query.filter_by(description=description).first()

    @classmethod
    def find_by_id(cls, id_):
         return cls.query.filter_by(id=id_).first()
    
    def get_materials(self):
        return [material.json() for material in self.materials]
