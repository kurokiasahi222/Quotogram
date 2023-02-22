from flask import *
import json
import os
from urllib.parse import quote_plus, urlencode
from authlib.integrations.flask_client import OAuth
from functools import wraps

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

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/profile")
def profile():
    return render_template("profile.html")
