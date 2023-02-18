from flask import Flask, render_template, redirect, session, url_for
import json
import os
from urllib.parse import quote_plus, urlencode
from authlib.integrations.flask_client import OAuth
from functools import wraps

from db import *

app = Flask(__name__)
app.secret_key = os.environ.get("APP_SECRET_KEY")

oauth = OAuth(app)

oauth.register(
    "auth0",
    client_id=os.environ.get("AUTH0_CLIENT_ID"),
    client_secret=os.environ.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{os.environ.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)

@app.before_first_request
def init():
    setup()  # call setup from the db.py file

@app.route("/")
def index():
    print(test_db_connection()) # TODO: remove later
    return render_template("index.html")

######### Auth0 stuff ########

# The funtion below can be used with an annotation @requires_auth  
# This will ensure that while visiting certain pages the users will be logged in or will have to log in
def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user' not in session:
            # Redirect to Login page here
            return redirect('/login')
        return f(*args, **kwargs)

    return decorated

@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )

@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    session["uid"] = token["userinfo"]["sid"]
    session["first_name"] = token["userinfo"]["given_name"]
    session["last_name"] = token["userinfo"]["family_name"]
    session["email"] = token["userinfo"]["email"]
    session["picture"] = token["userinfo"]["picture"]
    return redirect("/") # TODO: Change to logged in page


@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://" + os.environ.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("index", _external=True),
                "client_id": os.environ.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )