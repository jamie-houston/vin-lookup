import datetime

from PyPDF2.utils import PdfReadError

from app.telly_api import repository, vin_lookup, vin_generator
from result import Ok, Err

# Check next 200 possible vins (for international vins that won't be returned
RETRY_COUNT = 200


def find_missing_cars(start=0, limit=10):
    run_start = datetime.datetime.utcnow()
    missing_serials = repository.get_missing_serials()
    retries = start
    total = min(limit + start, len(missing_serials))
    found = []
    while retries < total:
        vins = vin_generator.get_next_vin_by_serial(missing_serials[retries])
        result = __find_vin__(vins)
        if result.is_ok():
            found.append(result.value.vin)
        retries += 1

    repository.log_scraper_run(len(found), run_start, "missing")
    return found


def get_next_batch(batch_size):
    run_start = datetime.datetime.utcnow()
    found = 0
    last_vin = repository.get_latest_car().vin
    print(f"running batch of {batch_size}")
    while found < batch_size:
        print(f"Getting car {found}")
        result = get_next_car(last_vin)
        if result.is_err():
            break
        last_vin = result.value.vin
        found += 1

    repository.log_scraper_run(found, run_start, "new")
    return {'found': found, 'start': run_start, 'end': datetime.datetime.utcnow()}


def get_next_car(last_vin):
    retries = 0
    while retries < RETRY_COUNT:
        next_vins = vin_generator.get_next_vin(last_vin)
        result = __find_vin__(next_vins)
        if result.is_ok():
            return result

        last_vin = next_vins[0]
        retries += 1

    return Err("No more vins")


def scrape_vin(vin):
    car, dealer, car_model = vin_lookup.scrape_vin(vin)
    repository.create_dealer(dealer)
    repository.create_car_model(car_model)
    repository.create_car(car)
    return car


def __find_vin__(next_vins):
    for vin_number in next_vins:
        print(f"trying {vin_number}")
        try:
            next_car = scrape_vin(vin_number)
            print(f"found {next_car.vin}")
            return Ok(next_car)
        except PdfReadError as e:
            print("not found")
    return Err("No results for vin")


