import os
from flask import Flask
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from config import app_config
from flask_caching import Cache

db = SQLAlchemy()
ma = Marshmallow()
cache = Cache()


def create_app(config_name):
    app = Flask(__name__)
    init_caching(app)

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
    cache_servers = os.environ.get('MEMCACHIER_SERVERS')
    # if cache_servers == None:
    cache.init_app(app, config={'CACHE_TYPE': 'simple'})
    # else:
    #     cache_user = os.environ.get('MEMCACHIER_USERNAME') or ''
    #     cache_pass = os.environ.get('MEMCACHIER_PASSWORD') or ''
    #     cache.init_app(app,
    #                    config={'CACHE_TYPE': 'saslmemcached',
    #                            'CACHE_MEMCACHED_SERVERS': cache_servers.split(','),
    #                            'CACHE_MEMCACHED_USERNAME': cache_user,
    #                            'CACHE_MEMCACHED_PASSWORD': cache_pass,
    #                            'CACHE_OPTIONS': {'behaviors': {
    #                                # Faster IO
    #                                'tcp_nodelay': True,
    #                                # Keep connection alive
    #                                'tcp_keepalive': True,
    #                                # Timeout for set/get requests
    #                                'connect_timeout': 2000,  # ms
    #                                'send_timeout': 750 * 1000,  # us
    #                                'receive_timeout': 750 * 1000,  # us
    #                                '_poll_timeout': 2000,  # ms
    #                                # Better failover
    #                                'ketama': True,
    #                                'remove_failed': 1,
    #                                'retry_timeout': 2,
    #                                'dead_timeout': 30}}})
