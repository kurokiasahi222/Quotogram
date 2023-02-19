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

# TODO: Delete this once we have actual queries
def test_db_connection():
    with get_db_cursor() as cur:
        cur.execute("SELECT 1=1")
        return cur.fetchall()

def get_posts(user_id, q=ALL_POSTS.format(user_id=user_id)):
    # make a SELECT query
    with get_db_cursor() as cur:
        current_app.logging.info("Executing query {}".format(q))
        cur.execute(q)
        return cur.fetchall()

def get_post_table_json():
    #jsonify the post table
    with get_db_cursor() as cur:
        cur.execute("select row_to_json(post) from post")
        return cur.fetchall()