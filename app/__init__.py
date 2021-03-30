# generic code used from flask documentation for application factory functionality
# source link: https://flask.palletsprojects.com/en/1.1.x/tutorial/factory/
import os

from flask import Flask
from . import db

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

    return app

  if __name__ == '__main__':
    # connect to database 
    # call function get_initial_data for each data table to get data formatted properly for inserting into tables
    # for loop - for tuple in data obj (returned from get_initial_data())
    #               execute SQL query with tuple as data arguments
    #               commit query to database
 
  