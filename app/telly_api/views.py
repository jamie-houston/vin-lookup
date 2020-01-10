from flask import request, jsonify

from app.models import CarSchema
from . import telly_api
from app.telly_api import repository, vin_generator, vin_service

car_schema = CarSchema()


# endpoint to create new car
@telly_api.route("/api/<vin>", methods=["GET"])
def add_car(vin):
    car = vin_service.scrape_vin(vin)

    return jsonify({'id': car.id, 'vin': car.vin})


# endpoint to show all cars
@telly_api.route("/api/cars", methods=["GET"])
def get_cars():
    all_cars = repository.get_cars()

    result = car_schema.dump(all_cars)

    return jsonify(result)


@telly_api.route("/api/update", methods=["GET"])
def update_cars():
    next_car = vin_service.get_next_car()

    result = car_schema.dump(next_car)
    return jsonify(result)


@telly_api.route("/api/next/<vin>", methods=["GET"])
def next_vin(vin):
    return jsonify(vin_generator.get_next_vin(vin))

