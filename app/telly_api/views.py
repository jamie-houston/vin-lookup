from flask import request, jsonify

from app.models import Car, CarSchema
from . import telly_api
from app.telly_api import repository, vin_lookup
from . import vin_generator

car_schema = CarSchema()


# endpoint to create new car
@telly_api.route("/api/<vin>", methods=["GET"])
def add_car(vin):
    car = scrape_vin(vin)

    return jsonify({'id': car.id, 'vin': car.vin})


def scrape_vin(vin):
    car, dealer, car_model = vin_lookup.scrape_vin(vin)
    repository.create_dealer(dealer)
    repository.create_car_model(car_model)
    repository.create_car(car)
    return car


# endpoint to show all cars
@telly_api.route("/cars", methods=["GET"])
def get_cars():
    all_cars = Car.query.all()

    result = car_schema.dump(all_cars)

    # return jsonify(result.data)
    return jsonify(result)


@telly_api.route("/update", methods=["GET"])
def update_cars():
    previous_car = repository.get_latest_car()
    next_car = None
    last_vin = previous_car.vin
    while (next_car == None):
        next_vins = vin_generator.get_next_vin(last_vin)
        next_car = find_vin(next_car, next_vins)
        last_vin = next_vins[0]

    result = car_schema.dump(next_car)
    return jsonify(result)


def find_vin(next_car, next_vins):
    for vin_number in next_vins:
        print(f"trying {vin_number}")
        try:
            next_car = scrape_vin(vin_number)
            print(f"found {next_car.vin}")
            break
        except:
            print("not yet")
    return next_car


@telly_api.route("/next/<vin>", methods=["GET"])
def next_vin(vin):
    return jsonify(vin_generator.get_next_vin(vin))
