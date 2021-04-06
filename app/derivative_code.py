# From endpoints.py
from flask import Flask, Blueprint, request, jsonify;
from app.db import get_db
from app.helper import *
import json

# From api/__init__.py
from .endpoints import *

# From helper/__init__.py
from .helper_functions import *

# from helper_functions.py
import os
import platform
import pprint
import json

# from app/__init__.py
# generic code used from flask documentation for application factory functionality
# source link: https://flask.palletsprojects.com/en/1.1.x/tutorial/factory/
import os

from flask import Flask
from . import db
import app.api as api
from flask_cors import CORS

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

	db.init_app(app)	# registers database with app

	app.register_blueprint(api.endpoints.bp)
	CORS(app)
	return app

# From db.py
# generic code used from flask documentation to set up a sqlite database instance 
# source link: https://flask.palletsprojects.com/en/1.1.x/tutorial/database/
import sqlite3 
import click
from flask import current_app, g
from flask.cli import with_appcontext
import app.data as data

def get_db():
	if 'db' not in g:
		g.db = sqlite3.connect(
			current_app.config['DATABASE'],
			detect_types=sqlite3.PARSE_DECLTYPES
		)
		g.db.row_factory = sqlite3.Row

	return g.db


def close_db(e=None):
	db = g.pop('db', None)

	if db is not None:
		db.close()

def init_db():
	db = get_db()

	with current_app.open_resource('schema.sql') as f:
		db.executescript(f.read().decode('utf8'))

@click.command('init-db')
@with_appcontext
def init_db_command():
	"""Clear the existing data and create new tables."""
	init_db()
	click.echo('Initialized the database.')

def init_app(app):
	app.teardown_appcontext(close_db)
	app.cli.add_command(init_db_command)

# from data/__init__.py
from .database_functions import *

# from database_functions.py
import csv

# requirements.txt 
click==7.1.2
Flask==1.1.2
Flask-Cors==3.0.10
itsdangerous==1.1.0
Jinja2==2.11.3
MarkupSafe==1.1.1
six==1.15.0
Werkzeug==1.0.1

