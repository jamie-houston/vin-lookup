import os
import requests
import io
import PyPDF2
from torrequest import TorRequest
from app.models import Car, CarModel, Dealer
import time

headers = {
    'cache-control': 'no-cache',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-gpc': '1',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'accept-language': 'en-US,en;q=0.9',
    'kiaws-api-key': '15724294-592e-4067-93af-515da5d1a5f2',
    'origin': 'https://www.kia.com',
    'Referer': 'https://www.kia.com/',
    'dnt': '1',
}

def scrape_vin(vin):
    MODEL = "MODEL/OPT.CODE"
    EXT_COLOR = "EXTERIOR COLOR"
    INT_COLOR = "INTERIOR COLOR"
    VIN = "VEHICLE ID NUMBER"
    PORT = "PORT OF ENTRY"
    SOLD_TO = "Sold To"
    SHIP_TO = "Ship To"
    url = f'https://prod.idc.kia.us/sticker/find/{vin}'
    MODEL_YEAR = "TELLURIDE"
    session = requests.session()
    r = session.get(url, headers=headers)
    f = io.BytesIO(r.content)
    p = PyPDF2.PdfFileReader(f)
    pdf_text = p.getPage(0).extractText()
    start = 0

    end = pdf_text.index(MODEL_YEAR)
    model_year = pdf_text[start:end]
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

    car = Car(vin, ext_color, int_color, model_code, opt_code, ship_to, ship_to, model_year)
    dealer = Dealer(ship_to, dealer_address, zip)
    car_model  = CarModel(model_code, car_description)
    return car, dealer, car_model

