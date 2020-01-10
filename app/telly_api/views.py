from flask import request, jsonify

from app.models import Car, CarSchema
from . import telly_api
from app.telly_api import repository, vin_lookup
from . import vin_generator

car_schema = CarSchema()


# endpoint to create new car
@telly_api.route("/api/<vin>", methods=["GET"])
def add_car(vin):
    car, dealer, car_model = vin_lookup.scrape_vin(vin)
    repository.create_dealer(dealer)
    repository.create_car_model(car_model)
    repository.create_car(car)

    return jsonify({'id': car.id, 'vin': car.vin})


# endpoint to show all cars
@telly_api.route("/cars", methods=["GET"])
def get_cars():
    all_cars = Car.query.all()

    result = car_schema.dump(all_cars)

    # return jsonify(result.data)
    return jsonify(result)

@telly_api.route("/update", methods=["GET"])
def update_cars():
    return 'wip'


@telly_api.route("/next/<vin>", methods=["GET"])
def next_vin(vin):
    return vin_generator.get_next_vin(vin)
