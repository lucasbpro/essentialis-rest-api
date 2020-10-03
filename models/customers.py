
from db import db                     # import SQLAlchemy object
from constants import constants       # constants dictionary

# defines the model for 'customer' table in db
class CustomerModel(db.Model):

    # name of the table in database
    __tablename__ = 'customers'

    # define columns in table
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(constants['MEDIUM_LENGTH']))
    email = db.Column(db.String(constants['MEDIUM_LENGTH']))   
    birth_date = db.Column(db.String(constants['SHORT_LENGTH']))

    # define relationships with other tables
    orders = db.relationship('OrderModel', lazy='dynamic')

    def __init__(self, name, email, birth_date):
        self.name = name
        self.email = email
        self.birth_date = birth_date

    def json(self):
        return  {
                'id'    : self.id,
                'name'  : self.name,
                'email' : self.email,
                'birth_date'  : self.birth_date,
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, id_):
        return cls.query.filter_by(id=id_).first()
