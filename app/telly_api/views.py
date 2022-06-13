from flask import request, jsonify

from app.models import CarSchema, DealerSchema
from . import telly_api
from app.telly_api import repository, vin_generator, vin_service
import requests
import time

car_schema = CarSchema()
cars_schema = CarSchema(many=True)
dealers_schema = DealerSchema(many=True)

# endpoint to create new car
@telly_api.route("/pdf/<vin>", methods=["GET"])
def dump_pdf(vin):
    url = f'https://www.kia.com/us/services/en/windowsticker/load/{vin}'
    r = requests.get(url)

    return r.content

# endpoint to create new car
@telly_api.route("/api/<vin>", methods=["GET"])
def add_car(vin):
    car = vin_service.scrape_vin(vin)
    time.sleep(5)
    print("sleeping 5")
    result = car_schema.dump(car)

    return jsonify(result)


# endpoint to show all cars
@telly_api.route("/api/car_list", methods=["GET"])
def get_car_list():
    all_cars = repository.get_car_list(request.args)
    total = len(repository.get_cars())

    result = cars_schema.dump(all_cars)

    return jsonify({'total': total, 'rows': result})


# endpoint to show all cars
@telly_api.route("/api/cars", methods=["GET"])
def get_cars():
    all_cars = repository.get_cars()

    result = cars_schema.dump(all_cars)

    return jsonify(result)

# endpoint to show recent cars
@telly_api.route("/api/cars/recent", methods=["GET"])
def get_cars_recent():
    cars_recent = repository.get_cars_recent()

    result = cars_schema.dump(cars_recent)

    return jsonify(result)


@telly_api.route("/api/update", methods=["GET"])
def update_cars():
    previous_car = repository.get_latest_car()
    next_car = vin_service.get_next_car(previous_car.vin)

    result = car_schema.dump(next_car)
    return jsonify(result)


@telly_api.route("/api/next/<vin>", methods=["GET"])
def next_vin(vin):
    return jsonify(vin_generator.get_next_vin(vin))


@telly_api.route("/api/dealers", methods=["GET"])
def get_dealers():
    dealers = repository.get_dealers()

    result = dealers_schema.dump(dealers)

    return jsonify(result)


@telly_api.route("/api/batch/<int:batch_size>")
def run_batch(batch_size):
    stats = vin_service.get_next_batch(batch_size)
    return jsonify(stats)


@telly_api.route("/api/stats")
def scraper_stats():
    stats = repository.get_scraper_stats()
    return jsonify(stats)


@telly_api.route("/api/missingcount")
def missing_count():
    result = repository.get_missing_serials()
    return jsonify(len(result))


@telly_api.route("/api/missing/<int:start>/<int:limit>")
def find_missing(start,limit):
    result = vin_service.find_missing_cars(start, limit)
    return jsonify(result)
