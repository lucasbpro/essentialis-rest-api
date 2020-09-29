
from db import db #, materials_by_recipe  # import SQLAlchemy object
from constants import constants         # constants dictionary

materials_by_recipe = db.Table('materials_by_recipe',
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipes.id'), primary_key=True),
    db.Column('material_id', db.Integer, db.ForeignKey('raw_materials.id'), primary_key=True)
)

# defines the model for 'raw_materials' table in db
class RawMaterialModel(db.Model):

    # name of the table in database
    __tablename__ = 'raw_materials'

    # define columns in table
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(constants['MEDIUM_LENGTH']))
    package_price = db.Column(db.Float(constants['PRICE_PRECISION']))
    package_amt = db.Column(db.Integer)
    unit_material = db.Column(db.String(constants['UNIT_LENGTH']))     # m, ml, L, g (unidades de medicao)
    stock_amt = db.Column(db.Integer)
    sell_by_date = db.Column(db.String(constants['SHORT_LENGTH']))

    # define relationships with other tables
    recipes = db.relationship('RecipeModel',
                               secondary=materials_by_recipe,
                               backref=db.backref('materials'),
                               lazy='dynamic')

    def __init__(self, description, package_price, package_amt,
                unit_material, stock_amt, sell_by_date):
        self.description = description
        self.package_price = package_price
        self.package_amt = package_amt
        self.unit_material = unit_material
        self.stock_amt = stock_amt
        self.sell_by_date = sell_by_date

    def json(self):
        return  {'id'           : self.id,
                 'description'  : self.description,
                 'package_price': self.package_price,
                 'package_amt'  : self.package_amt,
                 'unit_material': self.unit_material,
                 'stock_amt'    : self.stock_amt,
                 'sell_by'      : self.sell_by_date
                 }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(description=name).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
