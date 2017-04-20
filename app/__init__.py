import os
import random
import xxhash

from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.mail import Mail
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy

from config import config

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()


_asset_hash_cache_ = {}


def _calculate_asset_hash(asset_file, dev_mode):
    if dev_mode:
        return random.random()

    """
    1. calculate the hash of asset file, use the hash as version number to control(maximize) the HTTP cache.
    2. the hash value will be cached in memory until the python app server restarted.
    3. only process text asset file(js and css), no binary file(img, fonts) processed. ##Todo##
    """
    hash = _asset_hash_cache_.get(asset_file)

    if not hash:
        file = os.path.join(os.path.dirname(__file__), *[x for x in asset_file.split('/')])
        if os.path.isfile(file):
            with open(file, 'r', encoding='utf-8') as f:
                data = f.read()
                hash = xxhash.xxh64(data).hexdigest()
                _asset_hash_cache_[asset_file] = hash

    return hash


def _register_jinja_env_globals(app, dev_mode):
    app.jinja_env.globals['host'] = app.config.get('HOST_NAME')
    app.jinja_env.globals['asset_hash'] = _calculate_asset_hash
    if dev_mode:
        import socket
        app.jinja_env.globals['dev_mode'] = dev_mode
        app.jinja_env.globals['local_ip'] = lambda: socket.gethostbyname(socket.gethostname())


def _register_blueprints(app):
    from app.views import bp as root
    from app.api import bp as api

    app.register_blueprint(api, url_prefix='/api')


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)

    _register_blueprints(app)
    _register_jinja_env_globals(app, True)

    return app
