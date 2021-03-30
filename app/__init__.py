# generic code used from flask documentation for application factory functionality
# source link: https://flask.palletsprojects.com/en/1.1.x/tutorial/factory/
import os

from flask import Flask
from . import db
import app.api as api

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'game_db.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)  # registers database with app

    app.register_blueprint(api.endpoints.bp)
    return app


  