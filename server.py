from flask import *
from db import *

app = Flask(__name__)

@app.before_first_request
def init():
    setup()  # call setup from the db.py file

@app.route("/")
def hello_world():
    print(test_db_connection()) # TODO: remove later
    return render_template("index.html")

@app.route('/api') #default api route jsonifies post table
def default_table():
    return get_table_json('post')

@app.route('/api/<table_name>') #need to specify a table name here in the route
def table(table_name='post'):
    table_name = str(table_name)
    return get_table_json(table_name)
