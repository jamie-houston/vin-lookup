import os, sys
import json

from sqlalchemy.exc import InvalidRequestError

from app import create_app, db
from app.models import Car, Dealer, CarModel
from app.telly_api import repository, vin_generator


def import_file():
    config_name = os.getenv('FLASK_CONFIG')
    app = create_app(config_name)
    app.app_context().push()

    with open('data.json') as json_file:
        data = json.load(json_file)
        try:
            for data_row in data:
                vin = data_row['c'][0]['v']
                print(f'importing {vin}')
                if vin_generator.is_valid_vin(vin):
                    car_model = data_row['c'][4]['v']
                    opt_code = data_row['c'][5]['v']
                    ship_to = data_row['c'][6]['v']
                    sold_to = data_row['c'][7]['v']
                    address = data_row['c'][8]['v']
                    zip_code = data_row['c'][9]['v']
                    ext_color = data_row['c'][10]['v']
                    int_color = data_row['c'][11]['v']
                    created = data_row['c'][12]['v']
                    car = Car(vin, ext_color, int_color, car_model, opt_code, sold_to, ship_to)
                    dealer = Dealer(ship_to, address, zip_code)
                    repository.create_dealer(dealer)
                    repository.create_car(car)
        except InvalidRequestError as requestError:
            print(requestError)
        except:
            print(f'failed with {sys.exc_info()[0]}')


if __name__ == '__main__':
    import_file()
