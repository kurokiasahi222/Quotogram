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

def get_posts(uid, q=ALL_POSTS):
    # make a SELECT query
    q = q.format(user_id=uid)
    with get_db_cursor() as cur:
        current_app.logger.info("Executing query {}".format(q))
        cur.execute(q)
        return cur.fetchall()
    
def get_table_json(table_name="post"):
    #jsonify a table from the database
    with get_db_cursor() as cur:
        cur.execute("select row_to_json({name}) from {name}".format(name=table_name))
        # cur.execute("select row_to_json(%s) from %s", (table_name, table_name))
        return cur.fetchall()

def get_posts_by_category(category,q=POSTS_BY_CATEGORY):
    q = q.format(post_category=category) 
    with get_db_cursor() as cur:
        current_app.logger.info("Executing query {}".format(q))
        cur.execute(q)
        return cur.fetchall()

def check_user_id_in_database(user_id):
    # Check if a user is in the database
    q = """SELECT * FROM users WHERE user_id = '{user_id}'"""
    q = q.format(user_id=user_id)
    with get_db_cursor() as cur:
        current_app.logger.info("Executing query {}".format(q))
        cur.execute(q)
        return cur.fetchall()

def add_user(user_id,username,first_name,last_name,email,image):
    # This method is called to add the user to the users table and create a personal board for them 

    q_add_user = ADD_USER.format(user_id=user_id, username=username,first_name=first_name,
             last_name=last_name,email=email,profile_image=image)
    
    q_add_board = ADD_BOARD.format(user_id=user_id,title="Personal Board")
    
    with get_db_cursor(True) as cur: # we pass in True to commit after each insert
        current_app.logger.info("Executing query {}".format(q_add_user))
        cur.execute(q_add_user)
        
        current_app.logger.info("Executing query {}".format(q_add_board))
        cur.execute(q_add_board)

if __name__ == "__main__":
    # tests for get_posts, get_posts_by_category, get_post_table_json, and get_post_category_json
    app = Flask(__name__)
    with app.app_context():
        setup()
        # get_posts tests
        # print(get_posts("quotagram"))
        # print(get_posts("idk"))
        # # get_posts_by_category tests
        # print(get_posts_by_category("inspirational"))
        # print(get_posts_by_category("idk"))
        # json tests
        print(get_table_json())
        print(get_table_json("board"))
        print(get_table_json("followers"))
        print(get_table_json("post_category"))