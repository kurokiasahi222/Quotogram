from flask import *
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

@app.before_first_request
def init():
    setup()  # call setup from the db.py file

@app.route("/")
def index():
    user = None
    if 'user' in session:                   # check if user is logged in or not
        user = session['user']
    return render_template("index.html", user=user)

@app.route("/profile")
@requires_auth                              # need to be logged in to access this page
def profile():
    return render_template("profile.html", session=session["user"])

@app.route('/api')                          #default api route jsonifies post table
def default_table():
    return jsonify(get_table_json('post'))

@app.route('/api/<table_name>')             #need to specify a table name here in the route
def table(table_name='post'):
    try:
        table_name = str(table_name)
        return jsonify(get_table_json(table_name))
    except:
        # if the table doesn't exist then send back an 500 error
        abort(500)

######### Auth0 stuff ########

@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )

@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    session["uid"] = token["userinfo"]["sub"]
    session["username"] = token["userinfo"]["nickname"]
    session["first_name"] = token["userinfo"]["given_name"]
    session["last_name"] = token["userinfo"]["family_name"]
    session["email"] = token["userinfo"]["email"]
    session["picture"] = token["userinfo"]["picture"]

    # If the user is not in the database then add them to the database
    res = check_user_id_in_database(session["uid"])
    if len(res) == 0:    # if user is not in the database 
        add_user(session["uid"], session["username"], session["first_name"],
                session["last_name"], session["email"], session["picture"])

    return redirect("/profile") 


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
