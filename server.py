from flask import Flask, render_template
from db import *

app = Flask(__name__)

@app.before_first_request
def init():
    setup()  # call setup from the db.py file

@app.route("/")
def hello_world():
    print(test_db_connection()) # TODO: remove later
    return render_template("index.html")
