from flask import Blueprint

telly_api = Blueprint('telly_api', __name__)

from . import views
