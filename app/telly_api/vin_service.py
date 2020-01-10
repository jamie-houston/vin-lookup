from app.telly_api import repository, vin_lookup, vin_generator


def get_next_car():
    previous_car = repository.get_latest_car()
    next_car = None
    last_vin = previous_car.vin
    retries = 0
    while (next_car == None and retries < 5):
        next_vins = vin_generator.get_next_vin(last_vin)
        next_car = find_vin(next_car, next_vins)
        last_vin = next_vins[0]
        retries += 1

    return next_car or {}


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


def scrape_vin(vin):
    car, dealer, car_model = vin_lookup.scrape_vin(vin)
    repository.create_dealer(dealer)
    repository.create_car_model(car_model)
    repository.create_car(car)
    return car
