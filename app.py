# IMPORTS
from flask import Flask, abort, flash, redirect, request, url_for, render_template

# VARIABLES
app = Flask(__name__)
app.secret_key = "1qasdcvbhnji9jh8gf7yt24fgh0poijnwtfgnupiok3er"

#  Home Page


@app.route("/")
def index():
    return render_template("index.html", title="Home")

# Greeting Page


@app.route("/greet/<name>")
def hello_name(name):
    return render_template("greet.html", name=name, title="Hello")

# Addition Calculator


@app.route("/add", methods=["POST", "GET"])
def add():
    result = None
    if request.method == "POST":
        a = request.form.get("a", 0,  type=int)
        b = request.form.get("b", 0,  type=int)
        result = (a, b, a+b)
    return render_template("add.html", result=result)


posts = {
    2: ('For Breakfast I Had...', 'Scrambled eggs and orange juice. It was delicious'),
    3: ('For Lunch I Had...', 'Pizza. It tasted great'),
    4: ('For Dinner I Had...', 'Sushi. It was soo good')
}


@app.route("/posts/<int:post_id>")
def get_post(post_id):
    post = posts.get(post_id, None)
    if post is None:
        abort(404)
    return render_template("posts/get.html", post_title=post[0], post_content=post[1])


@app.route("/posts")
def get_all_posts():
    return render_template("posts/all.html", posts=posts.items())


@app.route("/posts/new", methods=['GET', 'POST'])
def new_post():
    if request.method == 'GET':
        return render_template("posts/new.html")
    title = request.form.get("title", None)
    content = request.form.get("content", None)
    if not (title and content):
        flash("Please enter all of the fields", "error")
        return redirect(url_for('new_post'))

    post_id = max(posts.keys()) + 1
    posts[post_id] = (title, content)
    return redirect(url_for("get_post", post_id=post_id))


# CRUD:
# Create
# Read
# Update
# Delete

# HTTP RESPONSE CODES
# See: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status#information_responses for all of the response codes
