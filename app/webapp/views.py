from flask import render_template
from app.telly_api import repository
from . import webapp
from app import cache


@webapp.route('/')
@cache.cached(timeout=60)
def index():
    scraper_stats = repository.get_scraper_stats()
    return render_template("cars.html", scraper_stats=scraper_stats)


@webapp.route('/all')
@cache.cached(timeout=60)
def cars_all():
    scraper_stats = repository.get_scraper_stats()
    return render_template("cars-all.html", scraper_stats=scraper_stats)

@webapp.route('/other')
@cache.cached(timeout=500)
def other():
    return render_template("other.html")


@webapp.route('/mobile')
@cache.cached(timeout=500)
def mobile():
    scraper_stats = repository.get_scraper_stats()
    cars = repository.get_cars()
    return render_template("mobile.html", cars=cars, scraper_stats=scraper_stats)


@webapp.route('/car/<vin>')
def car_info(vin):
    car = repository.get_car(vin)

    return render_template("car.html", car=car)


@webapp.route('/dealer/<dealer_code>')
def dealer_info(dealer_code):
    dealer = repository.get_dealer(dealer_code)
    cars = repository.get_dealer_cars(dealer_code)
    scraper_stats = repository.get_scraper_stats()
    return render_template("dealer.html", dealer=dealer, cars=cars, scraper_stats=scraper_stats)


@webapp.route('/dealers')
@cache.cached(timeout=60)
def dealers():
    scraper_stats = repository.get_scraper_stats()
    return render_template("dealers.html", scraper_stats=scraper_stats)


@webapp.route('/temp')
def temp_route():
    return render_template("temp.html")

@webapp.route('/cars2')
def cars2():
    scraper_stats = repository.get_scraper_stats()
    return render_template("cars2.html", scraper_stats=scraper_stats)

@webapp.route('/hof')
def hof():
    return render_template("hof.html")
