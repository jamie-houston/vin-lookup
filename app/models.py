from app import db, ma
import datetime
from sqlalchemy_utils import aggregated


class Car(db.Model):
    __tablename__ = 'cars'

    id = db.Column(db.Integer, primary_key=True)
    vin = db.Column(db.String())
    serial_number = db.Column(db.Integer)
    ext_color = db.Column(db.String())
    int_color = db.Column(db.String())
    car_model = db.Column(db.String(), db.ForeignKey('car_models.model_code'))
    opt_code = db.Column(db.String())
    sold_to = db.Column(db.String(), db.ForeignKey('dealers.dealer_code'))
    ship_to = db.Column(db.String())
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, vin, ext_color, int_color, car_model, opt_code, sold_to, ship_to):
        self.vin = vin
        self.ext_color = ext_color
        self.int_color = int_color
        self.car_model = car_model
        self.opt_code = opt_code
        self.sold_to = sold_to
        self.ship_to = ship_to
        self.serial_number = vin[len(vin)-6:]

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'vin': self.vin,
            'ext_color': self.ext_color,
            'int_color': self.int_color,
            'car_model': self.car_model,
            'opt_code': self.opt_code,
            'sold_to': self.sold_to,
            'ship_to': self.ship_to,
            'created_date': self.created_date
        }

class Dealer(db.Model):
    __tablename__ = "dealers"

    dealer_code = db.Column(db.String(), primary_key=True)
    address = db.Column(db.String())
    zip = db.Column(db.String())

    @aggregated('cars', db.Column(db.Integer))
    def car_count(self):
        return db.func.count('1')

    cars = db.relationship('Car', backref='dealer', lazy='dynamic')

    def __init__(self, dealer_code, address, zip):
        self.dealer_code = dealer_code
        self.address = address
        self.zip = zip

    def __repr__(self):
        return '<dealer_code {}>'.format(self.dealer_code)

    def serialize(self):
        return {
            'dealer_code': self.dealer_code,
            'address': self.address,
            'zip': self.zip,
            'car_count': self.car_count
        }


class CarModel(db.Model):
    __tablename__ = 'car_models'

    model_code = db.Column(db.String(), primary_key=True)
    description = db.Column(db.String())
    car = db.relationship('Car', backref='model_info', uselist=False)

    def __init__(self, model_code, description):
        self.model_code = model_code
        self.description = description

    def __repr__(self):
        return '<dealer_code {}>'.format(self.dealer_code)

    def serialize(self):
        return {
            'model_code': self.dealer_code,
            'description': self.address
        }


class ScraperLog(db.Model):
    __tablename__ = "scraper_logs"

    id = db.Column(db.Integer, primary_key=True)
    found_cars = db.Column(db.Integer)
    run_start = db.Column(db.DateTime)
    run_end = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    success = db.Column(db.Boolean)

    def __init__(self, found_cars, run_start, success):
        self.found_cars = found_cars
        self.run_start = run_start
        self.success = success


class CarSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('id', 'vin', 'ext_color', 'int_color', 'car_model', 'opt_code', 'sold_to', 'ship_tp', 'created_date', 'serial_number')


class DealerSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('dealer_code', 'address', 'zip', 'car_count')


class CarModelSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('model_code', 'description')

