from flask import *
import json
import os
import requests
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
    posts = None
    if 'user' in session:                   # check if user is logged in or not
        user = session['user']
        res = get_posts_logged_in(session["uid"]) 
        posts = json.loads(json.dumps(res))  # convert result to json string
    else:
        res = get_posts_not_logged_in()
        posts = json.loads(json.dumps(res))  # convert result to json string
    return render_template("index.html", user=user, posts=posts)

@app.route("/profile")
@requires_auth                              # need to be logged in to access this page
def profile():
    # Check for query string
    user = session['user']
    if 'username' in request.args:
        user_name = request.args.get("username")
        # check if the username exits 
        user_exists = check_username_in_database(user_name)
        if user_exists == []:
            # if the username does not exist then redirect to profile page
            return redirect('/profile')
        posts = get_user_posts_from_username(user_name)
        return render_template("profile.html", user=user, posts=posts)
    # If no query string, then get the user's profile
    posts, num_quotes, followers, num_followers, num_following = get_profile_data(session['uid']) 
    return render_template("profile.html", 
                           user=user,posts=posts, 
                           num_quotes=num_quotes,followers=followers, 
                           num_followers=num_followers, num_following=num_following)

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


@app.route('/api/delete', methods=["POST"])
def delete_quote():
    if 'user' in session:       # user has to be logged in
        body = request.get_json()
        quote_id = body['quote_id']
        if remove_post(session['uid'], quote_id):
            return jsonify({"status": "success"})
        else:
            return jsonify({"status": "failed"})
    else:
        abort(401) # send back an 401 Unauthorized message


@app.route('/api/like', methods=["POST"])
def like_quote():
    if 'user' in session:       # user has to be logged in
        body = request.get_json()
        quote_id = body["quote_id"]
        print("Attempting to like a quote with id: " + str(quote_id))
        success, num_likes = like_post(session['uid'], quote_id)

        if success:
            return jsonify({"status": "success", "num_likes": num_likes})
        else:
            return jsonify({"status": "failed", "num_likes": num_likes})
    else:
        abort(401) # send back an 401 Unauthorized message


@app.route("/explore", methods=["GET","POST"])
def explore():
    if request.method == 'GET':
        return render_template("explore.html", results=None)
    if request.method == 'POST':
        search_query = request.form.get("search")
        if 'user' in session:
            res  = search_quotes(session['uid'],search_query)
        else:
            res  = search_quotes(None,search_query)
        return render_template("explore.html", results=json.loads(json.dumps(res)))


@app.route("/new_post", methods=["POST"])
def new_post():
    user_id = session.get("uid", "jakdghjgdshJHBshjqUAs") # can change the default uid later
    quote = request.form.get("quote", "NOT FILLED OUT")
    quote_author = request.form.get("quote_author", "NOT FILLED OUT")
    context = request.form.get("context", "NOT FILLED OUT")
    add_post(user_id, quote, quote_author, context) # add the post to the post table

    # automatically follow the post after posting
    res = requests.get("http://127.0.0.1:5000/api/post")
    res = res.json()
    pid = -1
    for post in res: #get the most recent post
        if post['user_id'] == user_id:
            pid = max(post['post_id'], pid)
    follow_unfollow_post(user_id, pid)
    
    #category addition for a new post
    category = request.form.get('category', 'NOT FILLED OUT')
    add_post_category(pid, category)
    return redirect("/")

@app.route("/edit_post", methods=["POST"])
def edit_post():
    # I can't really test this without the form for 
    if 'user' in session:
        body = request.get_json()
        post_id = body.get('quote_id', -1)
        user_id = session.get("uid", "jakdghjgdshJHBshjqUAs")
        quote = request.form.get("quote", "NOT FILLED OUT")
        quote_author = request.form.get("quote_author", "NOT FILLED OUT")
        context = request.form.get("context", "NOT FILLED OUT")
        category = request.form.get('category', 'NOT FILLED OUT')
        edit_post(post_id, user_id, quote, quote_author, context)
        edit_post_category(post_id, category)
        return redirect("/")
    else:
        abort(401)
    

@app.route('/api/follow/post', methods=["POST"])
def add_post_to_following():
    if 'user' in session:               # user has to be logged in
        req = request.get_json()        # get the request object
        if 'quote_id' in req:
            follow_unfollow_post(session['uid'], req['quote_id']) # follow or unfollow the quote
            return jsonify({"status": 'success'})
        else: 
            return jsonify({"status": 'failed'})
    else:
        abort(401) # send back an 401 Unauthorized message
    
  
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

if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=True)