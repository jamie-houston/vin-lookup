from app.models import Car, Dealer, CarModel
from app import db


def create_car(car):
    existing_car = get_car(car.vin)
    if (existing_car == None):
        db.session.add(car)
        db.session.commit()

    return car


def create_dealer(dealer):
    existing_dealer = get_dealer(dealer.dealer_code)
    if (existing_dealer == None):
        db.session.add(dealer)
        db.session.commit()
    return dealer


def create_car_model(car_model):
    existing_model = get_model(car_model.model_code)
    if (existing_model == None):
        db.session.add(car_model)
        db.session.commit()
    return car_model


def get_all_cars():
    return Car.query.all()


def get_car(vin):
    car = Car.query.filter_by(vin=vin).first()
    return car


def get_dealer(dealer_code):
    dealer = Dealer.query.filter_by(dealer_code = dealer_code).first()
    return dealer


def get_model(model_code):
    car_model = CarModel.query.filter_by(model_code=model_code).first()
    return car_model
