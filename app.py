from flask import Flask
import requests
import io
import PyPDF2

app = Flask(__name__)


@app.route('/')
def hello_world():
    MODEL = "MODEL/OPT.CODE"
    EXT_COLOR = "EXTERIOR COLOR"
    INT_COLOR = "INTERIOR COLOR"
    VIN = "VEHICLE ID NUMBER"
    PORT = "PORT OF ENTRY"
    url = "https://www.kia.com/us/services/en/windowsticker/load/5XYP5DHC2LG067512"
    r = requests.get(url)
    f = io.BytesIO(r.content)
    p = PyPDF2.PdfFileReader(f)
    pdf_text = p.getPage(0).extractText()
    start = 0
    end = pdf_text.index(MODEL)
    model = pdf_text[start:end]

    start = end + len(MODEL) + 1
    end = pdf_text.index(EXT_COLOR)
    code = pdf_text[start:end]

    start = end + len(EXT_COLOR) + 1
    end = pdf_text.index(INT_COLOR)
    ext_color = pdf_text[start:end]

    start = end + len(INT_COLOR) + 1
    end = pdf_text.index(VIN)
    int_color = pdf_text[start:end]

    start = end + len(VIN) + 1
    end = pdf_text.index(PORT)
    vin = pdf_text[start:end]

    return f'model: {model} code: {code} ext: {ext_color} int: {int_color} vin: {vin}'


if __name__ == '__main__':
    app.run()
