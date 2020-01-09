import os
from flask import Flask
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from config import app_config

db = SQLAlchemy()
ma = Marshmallow()

def create_app(config_name):
    app = Flask(__name__)
    CORS(app)
    # app.config.from_object(app_config['production'])
    app.config.from_object(app_config['development'])
    app.config.from_pyfile('../config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    ma.init_app(app)

    from .webapp import webapp as webapp_blueprint
    app.register_blueprint(webapp_blueprint)

    from .telly_api import telly_api as telly_api_blueprint
    app.register_blueprint(telly_api_blueprint)
    return app
