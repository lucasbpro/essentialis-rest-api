
from db import db                     # import SQLAlchemy object
from constants import constants       # constants dictionary
from datetime import datetime

# defines the model for 'orders' table in db
class OrderModel(db.Model):

    # name of the table in database
    __tablename__ = 'orders'

    # define columns in table
    id = db.Column(db.Integer, primary_key=True);
    product_id = db.Column(db.Integer, db.ForeignKey('recipes.id'));
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'));
    order_total = db.Column(db.String(constants['SHORT_LENGTH']));
    status_fabrication = db.Column(db.String(constants['MEDIUM_LENGTH']));
    status_payment = db.Column(db.String(constants['MEDIUM_LENGTH']));
    order_date = db.Column(db.String(constants['MEDIUM_LENGTH']));
    notes = db.Column(db.String(constants['MEDIUM_LENGTH']));

    # define relationships with other tables
    product = db.relationship('RecipeModel');
    customer = db.relationship('CustomerModel');

    def __init__(self, product_id, customer_id, notes):
        self.product_id = product_id;
        self.customer_id = customer_id;
        self.notes = notes;
        self.order_total = 0;
        self.status_fabrication = "Fabricação a iniciar";
        self.status_payment = "Pagamento pendente";
        self.order_date = datetime.now().strftime("%d/%m/%Y %H:%M");
        self.notes = notes;


    def json(self):
        return  {
                'id' : self.id,
                'product_id' : self.product_id,
                'customer_id' : self.customer_id,
                'notes' : self.notes,
                'order_total' : self.order_total,
                'status_fabrication' : self.status_fabrication,
                'status_payment' : self.status_payment,
                'order_date' : self.order_date,
                'notes' : self.notes
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
