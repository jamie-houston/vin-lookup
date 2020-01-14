from flask import render_template
from app.telly_api import repository
from . import webapp
from app import cache


@webapp.route('/')
@cache.cached(timeout=50)
def index():
    return render_template("cars.html")


@webapp.route('/car/<vin>')
def car_info(vin):
    car = repository.get_car(vin)

    return render_template("car.html", car=car)


@webapp.route('/dealer/<dealer_code>')
def dealer_info(dealer_code):
    dealer = repository.get_dealer(dealer_code)
    cars = repository.get_dealer_cars(dealer_code)

    return render_template("dealer.html", dealer=dealer, cars=cars)


@webapp.route('/dealers')
@cache.cached(timeout=50)
def dealers():
    return render_template("dealers.html")


