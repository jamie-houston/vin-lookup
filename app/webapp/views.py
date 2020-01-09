from flask import render_template

from app.telly_api import repository
from . import webapp


@webapp.route('/')
def index():
    all_cars = repository.get_all_cars()
    return render_template("index.html", cars=all_cars)


@webapp.route('/<vin>')
def list_items(vin):
    car = repository.get_car(vin)

    return render_template("items.html", car=car)
