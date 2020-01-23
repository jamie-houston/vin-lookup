from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql.expression import func
from sqlalchemy.sql import text
from app.models import Car, Dealer, CarModel, ScraperLog
from app import db, cache


def create_car(car):
    existing_car = get_car(car.vin)
    if (existing_car == None):
        try:
            db.session.add(car)
            db.session.commit()
            cache.delete_memoized(__get_cars_from_db__)
        except IntegrityError as e:
            print(f"Error creating car {e}")
            db.session().rollback()

    return car


def create_dealer(dealer):
    existing_dealer = get_dealer(dealer.dealer_code)
    if (existing_dealer == None):
        try:
            db.session.add(dealer)
            db.session.commit()
            cache.delete_memoized(__get_dealers_from_db__)
        except IntegrityError as e:
            print(f"Error creating dealer {e}")
            db.session.rollback()
    return dealer


def create_car_model(car_model):
    existing_model = get_model(car_model.model_code)
    if (existing_model == None):
        db.session.add(car_model)
        db.session.commit()
    return car_model


def get_car_list(args={}):
    search = args.get("search")
    sort = args.get("sort")
    order = args.get("order", 'created_date')
    offset = args.get("offset", 0, type=int)
    limit = args.get("limit", 10, type=int)
    page = 1 if offset == 0 else offset / limit + 1
    return Car.query.order_by(text(f'{sort} {order}')).paginate(page, limit).items


def get_cars():
    return __get_cars_from_db__()


def get_car(vin):
    car = Car.query.filter_by(vin=vin).first()
    return car


def get_dealer(dealer_code):
    dealer = Dealer.query.filter_by(dealer_code=dealer_code).first()
    return dealer


def get_model(model_code):
    car_model = CarModel.query.filter_by(model_code=model_code).first()
    return car_model


def get_latest_car():
    max_date = db.session.query(func.max(Car.created_date)).first()
    return Car.query.filter_by(created_date=max_date).first()


def get_dealers():
    return __get_dealers_from_db__()


def get_dealer_cars(dealer_code):
    cars = Car.query.filter_by(ship_to=dealer_code).all()
    return cars


def log_scraper_run(found_cars, run_start, success=True):
    db.session.add(ScraperLog(found_cars, run_start, success))
    db.session.commit()


@cache.memoize()
def __get_dealers_from_db__():
    dealers = Dealer.query.order_by('dealer_code').all()
    return dealers


@cache.memoize()
def __get_cars_from_db__():
    return Car.query.order_by(Car.created_date.desc()).all()
