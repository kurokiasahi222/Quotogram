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
            last_name,image,email))


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


def get_posts_not_logged_in():
   with get_db_cursor() as cur:
       q = "SELECT row_to_json(t) FROM ("+ POSTS_NOT_LOGGED_IN +") t"
       current_app.logger.info("Executing query {}".format(q))
       cur.execute(q)
       result = cur.fetchall()
       return [ item[0] for item in result] # return as a list of dictionaries


def remove_post(user_id, quote_id):
    with get_db_cursor(True) as cur: 
        verify_query = "SELECT user_id FROM post WHERE post_id = %s"
        delete_query = "DELETE FROM post WHERE post_id = %s AND user_id = %s"

        # Get the user_id associated with the quote_id
        current_app.logger.info("Executing query {}".format(verify_query % (quote_id,)))
        cur.execute(verify_query, (quote_id,))
        res = cur.fetchall()
        if len(res) > 0: 
            if res[0][0] == user_id:    # check if the user_id of the requester matches the owner's user_id
                current_app.logger.info("Executing query {}".format(delete_query % (quote_id,user_id)))
                cur.execute(delete_query, (quote_id,user_id))
                return True
            else:
                current_app.logger.info("Received an Unauthorized request: User tried to delete someone else's post")
                return False
        return False


def like_post(user_id, post_id):
    with get_db_cursor(True) as cur:
        user_liked = False
        status = False
        # Get if user has liked the post
        try:
            q = "SELECT * FROM post_like WHERE post_id = %s"
            cur.execute(q, (post_id,))
            res = cur.fetchall()
            user_liked = user_id in [item[1] for item in res]

        except Exception as e:
            current_app.logger.error(e)

        if not user_liked:
            q = "INSERT INTO post_like (post_id,user_id) VALUES (%s,%s)"
        else:
            q = "DELETE FROM post_like WHERE post_id = %s AND user_id = %s"
        
        try:
            current_app.logger.info("Executing query {}".format(q % (post_id, user_id)))
            cur.execute(q, (post_id, user_id))

            status = True
        except Exception as e:
            current_app.logger.error(e)
        
        num_likes = 0
        try: 
            cur.execute(POST_LIKES, (post_id,))
            num_likes = cur.fetchone()[0]
        except Exception as e:
            current_app.logger.error(e)
        print("Found the number of likes for this post: {}".format(num_likes))

        return status, num_likes

def follow_unfollow_post(user_id, post_id):
    with get_db_cursor(True) as cur:
        # Depending on whether the user already follows the quote or not INSERT OR DELETE
        #   if user is not following we insert into post_following table
        #   else we delete row from  post_following table
        # Check QUOTE_FOLLOW_UNFOLLOW for how the query handles this in database
        current_app.logger.info("Executing query {}".format(QUOTE_FOLLOW_UNFOLLOW %  (user_id,post_id)))
        cur.execute(QUOTE_FOLLOW_UNFOLLOW, (user_id,post_id))

def search_quotes(user_id, search_text):
    with get_db_cursor() as cur:
        # We are performing OR operations of all words inputed 
        # So the query FULL_TEXT_SEARCH's search_query requires words to be separated by | 
        search_words = search_text.split()                      # split at space and get words into a list
        search_text = " | ".join(search_words)                  # join the list into a string separated by |
        
        current_app.logger.info("Executing query {}".format(FULL_TEXT_SEARCH %  {"user_id":user_id, "search_query":search_text}))
        cur.execute(FULL_TEXT_SEARCH,  {"user_id":user_id, "search_query":search_text})
        result = cur.fetchall()
        return [ item[0] for item in result] # return as a list of dictionaries
    
def follow_unfollow_user(user_id, followed_user_id):
    with get_db_cursor(True) as cur:
        # Depending on whether the user already follows the user or not INSERT OR DELETE
        #   if user is not following we insert into followers table
        #   else we delete row from  followers table
        # Check FOLLOW_UNFOLLOW_USER for how the query handles this in database
        current_app.logger.info("Executing query {}".format(FOLLOW_UNFOLLOW_USER %  (user_id,followed_user_id)))
        cur.execute(FOLLOW_UNFOLLOW_USER, (user_id,followed_user_id))
