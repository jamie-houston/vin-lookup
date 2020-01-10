from flask import render_template

from app.telly_api import repository
from . import webapp


@webapp.route('/')
def index():
    all_cars = repository.get_cars()
    all_dealers = repository.get_dealers()
    return render_template("cars.html", cars=all_cars, dealers=all_dealers)


@webapp.route('/car/<vin>')
def car_info(vin):
    car = repository.get_car(vin)

    return render_template("car.html", car=car)


@webapp.route('/dealer/<dealer_code>')
def dealer_info(dealer_code):
    dealer = repository.get_dealer(dealer_code)
    cars = repository.get_dealer_cars(dealer_code)

    return render_template("dealer.html", dealer=dealer, cars=cars)


