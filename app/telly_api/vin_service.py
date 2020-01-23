import datetime
from app.telly_api import repository, vin_lookup, vin_generator


def get_next_batch(batch_size):
    run_start = datetime.datetime.utcnow()
    found = 0
    next_car = None
    print(f"running batch of {batch_size}")
    while next_car is not {} and found < batch_size:
        print(f"Getting car {found}")
        next_car = get_next_car()
        found += 1

    repository.log_scraper_run(found, run_start)
    return {'found': found, 'start': run_start, 'end': datetime.datetime.utcnow()}


def get_next_car():
    previous_car = repository.get_latest_car()
    next_car = None
    last_vin = previous_car.vin
    retries = 0
    # Check next 200 possible vins (for international vins that won't be returned
    while next_car == None and retries < 200:
        next_vins = vin_generator.get_next_vin(last_vin)
        next_car = __find_vin__(next_car, next_vins)
        last_vin = next_vins[0]
        retries += 1

    return next_car or {}


def scrape_vin(vin):
    car, dealer, car_model = vin_lookup.scrape_vin(vin)
    repository.create_dealer(dealer)
    repository.create_car_model(car_model)
    repository.create_car(car)
    return car


def __find_vin__(next_car, next_vins):
    for vin_number in next_vins:
        print(f"trying {vin_number}")
        try:
            next_car = scrape_vin(vin_number)
            print(f"found {next_car.vin}")
            break
        except:
            print("not found")
    return next_car


