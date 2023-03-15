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

 
def requires_auth(f):
    """The function can be used with an annotation @requires_auth. This will ensure that while visiting 
    certain pages the users will be logged in or will have to log in"""
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
    page = int(request.args.get("page", 1)) - 1
    user = None
    posts = None
    qod = None

    num_pages = get_num_posts() // 24 + 1
    if(page < 0 or page >= num_pages):
        page = 0

    if 'user' in session:                   # check if user is logged in or not
        user = session['user']
        res = get_posts_logged_in(session["uid"], page=page)
        posts = json.loads(json.dumps(res))  # convert result to json string
        qod = json.loads(json.dumps(get_qod(True, session["uid"])))
    else:
        res = get_posts_not_logged_in(page=page)
        posts = json.loads(json.dumps(res))  # convert result to json string
        qod = json.loads(json.dumps(get_qod(False)))
    print(qod)
    return render_template("index.html", user=user, posts=posts, qod=qod, page=page+1, num_pages=num_pages)


@app.route("/profile")
@requires_auth                              # need to be logged in to access this page
def profile():
    # Check for query string
    user = session['user']
    authzero = 'google-oauth2|'
    if 'userid' in request.args:
        userid = request.args.get('userid')
        # check if the username exits 
        user_exists = check_user_id_in_database(authzero + userid)
        if user_exists == [] or userid == session['uid']:
            # if the userid does not exist then redirect to profile page
            return redirect('/profile')
        posts = get_user_posts_from_id(authzero + userid)
        followers = get_followers(authzero + userid)
        user_info = get_user_info(authzero + userid)
        print(user_info)
        return render_template("profile_dynamic.html", user=user, posts=posts, num_quotes=len(posts), num_followers=len(followers), other_user=user_info)
    # If no query string, then get the user's profile
    posts, followers, num_quotes, num_followers, num_following = get_profile_data(session['uid']) 
    print("My posts" + str(posts))
    return render_template("profile_dynamic.html", 
                           user=user,posts=posts, 
                           num_quotes=num_quotes,followers=followers, 
                           num_followers=num_followers, num_following=num_following)


@app.route("/followers")
@requires_auth                              # need to be logged in to access this page
def followers():
    user = session['user']
    followers = get_user_followers(session['uid'])
    num_followers = get_num_followers(session['uid']) 
    num_quotes = get_posts_number(session['uid'])
    return render_template("followers.html", user=user, followers=followers, num_quotes=num_quotes, num_followers=num_followers)


@app.route("/following")
@requires_auth                              # need to be logged in to access this page
def following():
    user = session['user']
    following = get_user_following(session['uid'])
    num_followers = get_num_followers(session['uid']) 
    num_quotes = get_posts_number(session['uid'])
    return render_template("following.html", user=user, following=following, num_quotes=num_quotes, num_followers=num_followers)


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
    print("Attempting to delete a quote")
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
    user = None
    if 'user' in session:                   # check if user is logged in or not
        user = session['user']
    if request.method == 'GET':
        return render_template("explore.html",user=user, results=None)
    if request.method == 'POST':
        search_query = request.form.get("search")
        if 'user' in session:
            res  = search_quotes(session['uid'],search_query)
        else:
            res  = search_quotes(None,search_query)
        return render_template("explore.html",user=user, results=json.loads(json.dumps(res)))


@app.route("/new_post", methods=["POST"])
def new_post():
    user_id = session.get("uid", "jakdghjgdshJHBshjqUAs") # can change the default uid later
    quote = request.form.get("quote", "NOT FILLED OUT")
    quote_author = request.form.get("quote_author", "NOT FILLED OUT")
    context = request.form.get("context", "NOT FILLED OUT")
    add_post(user_id, quote, quote_author, context) # add the post to the post table

    # automatically follow the post after posting
    res = get_table_json("post")
    pid = -1
    for post in res: # get the most recent post
        if post['user_id'] == user_id:
            pid = max(post['post_id'], pid)
    follow_unfollow_post(user_id, pid)
    
    #category addition for a new post
    categories = request.form.getlist('post-category')
    if len(categories) > 0:
        for category in categories:
            add_post_category(pid, category)
    return redirect("/")


@app.route("/edit_post", methods=["POST"])
def edit_post():
    if 'user' in session:
        # edit the post within the post table
        user_id = session.get("uid", "jakdghjgdshJHBshjqUAs")
        post_id = request.form.get("quote_id", "NOT FILLED OUT")
        quote = request.form.get("quote", "NOT FILLED OUT")
        quote_author = request.form.get("quote_author", "NOT FILLED OUT")
        context = request.form.get("context", "NOT FILLED OUT")
        edit_post_db(post_id, user_id, quote, quote_author, context)

        # edit the categories(remove post from post_category table then re-add with new categories)
        remove_from_post_category(post_id)
        categories = request.form.getlist('post-category')
        if len(categories) > 0:
            for category in categories:
                add_post_category(post_id, category)
        return redirect("/")
    else:
        abort(401)
    

@app.route('/api/follow/post', methods=["POST"])
def add_post_to_following():
    if 'user' in session:               # user has to be logged in
        req = request.get_json()        # get the request object
        if 'quote_id' in req:
            res = follow_unfollow_post(session['uid'], req['quote_id']) # follow or unfollow the quote
            if res:
                return jsonify({"status": 'success'})
            else:
                return jsonify({"status": 'failed'})
        else: 
            return jsonify({"status": 'failed'})
    else:
        abort(401) # send back an 401 Unauthorized message
    

@app.route("/api/follow/user", methods=["POST"])
@requires_auth 
def perform_follow_unfollow():
    req = request.get_json() # get the request object
    if 'quote_id' in req:
        followed_user_id = str(req['quote_id'])
        follow_unfollow_user(session['uid'], followed_user_id) # follow or unfollow the user
        return jsonify({"status": 'success'})
    else:
        return jsonify({"status": 'failed'})


@app.route("/api/post-category/<post_id>")
def fetch_post_categories(post_id):
    return jsonify({
        "categories": get_post_categories(post_id)
        })
 

@app.route("/api/is-following/<user_id>")
@requires_auth
def fetch_if_following(user_id):
    other_user = 'google-oauth2|'+str(user_id)
    return jsonify(get_is_following(session['uid'],other_user)) 


######### Error Handling Functions ########


@app.errorhandler(404)
def page_not_found(e):
    user = None
    if 'user' in session:
        user = session['user']
    return render_template("errors/404.html", user=user), 404


@app.errorhandler(403)
def forbidden(e):
    user = None
    if 'user' in session:
        user = session['user']
    return render_template("errors/403.html", user=user), 403


@app.errorhandler(410)
def gone(e):
    user = None
    if 'user' in session:
        user = session['user']
    return render_template("errors/410.html", user=user), 410


@app.errorhandler(500)
def internal_server_error(e):
    user = None
    if 'user' in session:
        user = session['user']
    return render_template("errors/500.html", user=user), 500


app.register_error_handler(404, page_not_found)
app.register_error_handler(403, forbidden)
app.register_error_handler(410, gone)
app.register_error_handler(500, internal_server_error)


######### Auth0 Functions ########


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
    