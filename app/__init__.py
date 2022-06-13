import os
from flask import Flask
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from config import app_config
from flask_caching import Cache
from flask_moment import Moment
from flask_cache_buster import CacheBuster

db = SQLAlchemy()
ma = Marshmallow()
cache = Cache()


def create_app(config_name):
    app = Flask(__name__)
    init_caching(app)
    moment = Moment(app)

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


def init_caching(app):
    # add versioning to client-side files
    client_cache_config = {
        'extensions': ['.js', '.css'],
        'hash_size': 10
    }

    cache_buster = CacheBuster(config=client_cache_config)
    cache_buster.register_cache_buster(app)

    # Use redis for server side caching
    redis_url = os.getenv("REDISCLOUD_URL")
    if redis_url == None:
        cache.init_app(app, config={'CACHE_TYPE': 'simple'})
    else:
        cache.init_app(app,
                       config={'CACHE_TYPE': 'redis',
                       'CACHE_REDIS_URL': redis_url})
