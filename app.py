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
    url = "https://www.kia.com/us/services/en/windowsticker/load/5XYP5DHC2LG067512"
    r = requests.get(url)
    f = io.BytesIO(r.content)
    p = PyPDF2.PdfFileReader(f)
    pdf_text = p.getPage(0).extractText()
    return pdf_text[0:pdf_text.index(MODEL)]


if __name__ == '__main__':
    app.run()
