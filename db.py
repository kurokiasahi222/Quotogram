""" database access
docs:
* http://initd.org/psycopg/docs/
* http://initd.org/psycopg/docs/pool.html
* http://initd.org/psycopg/docs/extras.html#dictionary-like-cursor
"""

from contextlib import contextmanager
import logging
import os
from flask import *

import psycopg2
from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extras import DictCursor

from query_constants import * 

pool = None

def setup():
    global pool
    DATABASE_URL = os.environ['DATABASE_URL']
    current_app.logger.info(f"creating db connection pool")
    pool = ThreadedConnectionPool(1, 10, dsn=DATABASE_URL, sslmode='require')


@contextmanager
def get_db_connection():
    try:
        connection = pool.getconn()
        yield connection
    finally:
        pool.putconn(connection)


@contextmanager
def get_db_cursor(commit=False):
    with get_db_connection() as connection:
      cursor = connection.cursor(cursor_factory=DictCursor)
      # cursor = connection.cursor()
      try:
          yield cursor
          if commit:
              connection.commit()
      finally:
          cursor.close()

def get_posts(uid, q=ALL_POSTS):  #TODO: Fix to get USER_POSTS and POSTS_FOLLOWING with the post likes
    # make a SELECT query
    with get_db_cursor() as cur:
        current_app.logger.info("Executing query {}".format(q))
        cur.execute(q, (uid,uid,uid))
        return cur.fetchall()

def get_table_json(table_name="post"):
    #jsonify a table from the database
    with get_db_cursor() as cur:
        q = "select row_to_json(%s) from %s"
        current_app.logger.info("Executing query {}".format(q % (table_name, table_name)))
        cur.execute(q % (table_name, table_name))
        result =  cur.fetchall()
        return [ item[0] for item in result]  # return as a list of dictionaries not a nested list

def check_user_id_in_database(user_id):
    # Check if a user is in the database
    with get_db_cursor() as cur:
        current_app.logger.info("Executing query SELECT * FROM users WHERE user_id = {}".format(user_id))
        cur.execute("SELECT * FROM users WHERE user_id = %s ", (user_id,))
        return cur.fetchall()

def add_user(user_id,username,first_name,last_name,email,image):
    # This method is called to add the user to the users table
    with get_db_cursor(True) as cur: # we pass in True to commit after each insert
        current_app.logger.info("Executing query {}".format(ADD_USER % (user_id,username,first_name,
            last_name,email,image)))
        cur.execute(ADD_USER, (user_id,username,first_name,
            last_name,email,image))

def add_post(user_id, quote, quote_author, context):
    with get_db_cursor(True) as cur:
        current_app.logger.info("Executing query INSERT INTO post (user_id, quote, quote_author, context) VALUES ({user_id}, {quote}, {quote_author}, {context})"
            .format(user_id=user_id, quote=quote, quote_author=quote_author, context=context))
        cur.execute("INSERT INTO post (user_id, quote, quote_author, context) VALUES (%s, %s, %s, %s)", 
            (user_id, quote, quote_author, context))
    
def get_posts_logged_in(user_id):
    with get_db_cursor() as cur:
        q = "SELECT row_to_json(t) FROM ("+ POSTS_LOGGED_IN +") t"
        current_app.logger.info("Executing query {}".format(q % (user_id,user_id)))
        cur.execute(q, (user_id,user_id))
        result = cur.fetchall()
        return [ item[0] for item in result] # return as a list of dictionaries

if __name__ == "__main__":
    app = Flask(__name__)
    with app.app_context():
        setup()
        add_post("jakdghjgdshJHBshjqUAs", "Testing add_post function", "not-anwaar", "idk")
