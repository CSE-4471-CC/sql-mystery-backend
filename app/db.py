# lines 4 - 42 are generic code used from flask documentation to set up a sqlite database instance 
# source link: https://flask.palletsprojects.com/en/1.1.x/tutorial/database/
# lines starting at 43 are original code 
import sqlite3 
import click
from flask import current_app, g
from flask.cli import with_appcontext

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

  # uncomment line 45 when you are ready to implement the function
  #if __name__ == '__main__':
    # connect to database 
    # call function get_initial_data for each data table to get data formatted properly for inserting into tables
    # for loop - for tuple in data obj (returned from get_initial_data())
    #               execute SQL query with tuple as data arguments
    #               commit query to database
 
    