
import requests
import io
import PyPDF2
from app.models import Car, CarModel, Dealer

def scrape_vin(vin):
    MODEL = "MODEL/OPT.CODE"
    EXT_COLOR = "EXTERIOR COLOR"
    INT_COLOR = "INTERIOR COLOR"
    VIN = "VEHICLE ID NUMBER"
    PORT = "PORT OF ENTRY"
    SOLD_TO = "Sold To"
    SHIP_TO = "Ship To"
    url = f'https://www.kia.com/us/services/en/windowsticker/load/{vin}'
    r = requests.get(url)
    f = io.BytesIO(r.content)
    p = PyPDF2.PdfFileReader(f)
    pdf_text = p.getPage(0).extractText()
    start = 0
    end = pdf_text.index(MODEL)
    car_description = pdf_text[start:end]

    start = end + len(MODEL) + 1
    end = pdf_text.index(EXT_COLOR)
    vin_code = [x.strip() for x in pdf_text[start:end].split('/')]
    model_code = vin_code[0]
    opt_code = vin_code[1]

    start = end + len(EXT_COLOR) + 1
    end = pdf_text.index(INT_COLOR)
    ext_color = pdf_text[start:end]

    start = end + len(INT_COLOR) + 1
    end = pdf_text.index(VIN)
    int_color = pdf_text[start:end]

    start = end + len(VIN) + 1
    end = pdf_text.index(PORT)
    vin = pdf_text[start:end]

    start = pdf_text.index(SOLD_TO) + len(SOLD_TO) + 2
    end = pdf_text.index(SHIP_TO)
    sold_to = pdf_text[start:end]

    start = end + len(SHIP_TO) + 2
    end = start + 5
    ship_to = pdf_text[start:end]
    dealer_address = sold_to.replace(ship_to, '')
    zip = dealer_address[len(dealer_address)-5:]

    car = Car(vin, ext_color, int_color, model_code, opt_code, ship_to, ship_to)
    dealer = Dealer(ship_to, dealer_address, zip)
    car_model  = CarModel(model_code, car_description)
    return car, dealer, car_model

