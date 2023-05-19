import os
from dotenv import load_dotenv
import pymysql
import click
from flask import current_app, g
from flask.cli import with_appcontext

# .env 파일 auto load
load_dotenv()


def get_db():
    if 'db' not in g:
        g.db = pymysql.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PWD'),
            database=os.getenv('DB_NAME'),
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor
            # current_app.config['DATABASE'],
        )
        return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

# function to get parsed query from sql file
def get_query_from_file(filename):
    from os import path

    # File did not exist
    if path.isfile(filename) is False:
        print("File load error : {}".format(filename))
        return False

    else:
        with open(filename, "r") as sql_file:
            # Split file in list
            ret = sql_file.read().split(';')
            # drop last empty entry
            ret.pop()
            sql_file.close()
            return ret

# Function to initialize the database
def init_db():
    db = get_db()
    query_list = get_query_from_file('flaskr/schema.sql')

    if query_list is not False :
        with db.cursor() as cursor:
            for idx, query in enumerate(query_list):
                cursor.execute(query + ';')
                print('query : ' + str(idx) + query + '\n')
        db.commit()
        click.echo('Insert query.')
    else:
        click.echo('Failed to create default table')
@click.command('init-db')
@with_appcontext
def init_db_command():
    # Delete existing data and re-create tables.
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
