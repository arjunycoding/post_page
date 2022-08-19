# IMPORTS
from flask import Flask, abort, flash, redirect, request, url_for, render_template

# APP
app = Flask(__name__)
app.secret_key = "ærjüń"

# VARIABLES
posts = {
    1: ('For Breakfast I Had...', 'Scrambled eggs and orange juice. It was delicious'),
    2: ('For Lunch I Had...', 'Pizza. It tasted great'),
    3: ('For Dinner I Had...', 'Sushi. It was soo good')
}


@app.route("/")
# VIEW ALL POSTS
def get_all_posts():
    return render_template("all.html", posts=posts.items())


@app.route("/posts/<int:post_id>")
# VIEW SPECIFIC POST
def get_post(post_id):
    post = posts.get(post_id, None)
    if post is None:
        abort(404)
    return render_template("get.html", post_title=post[0], post_content=post[1], post_id=post_id)


@app.route("/posts/new", methods=['GET', 'POST'])
# NEW POST
def new_post():
    if request.method == 'GET':
        return render_template("new.html")
    title = request.form.get("title", None)
    content = request.form.get("content", None)
    if not (title and content):
        flash("Please enter all of the fields", "alert-danger")
        return redirect(url_for('new_post'))

    post_id = None
    if len(posts) == 0:
        post_id = 0
    else:
        post_id = max(posts.keys()) + 1
    posts[post_id] = (title, content)
    flash("Your post has successfully been created", "alert-success")
    return redirect(url_for("get_all_posts", posts=posts.items()))

@app.route("/posts/<int:post_id>/update", methods=['GET', 'POST'])
# UPDATE POST
def update_post(post_id):
    if request.method == 'GET':
        post = posts.get(post_id, None)

        if post == None:
            return redirect(url_for("get_all_posts", posts=posts.items()))
        
        print(posts[post_id][1])
        return render_template("new.html", post_title=posts[post_id][0], post_content=posts[post_id][1], value="Update Post", title="Update Post")


    title = request.form.get("title", None)
    content = request.form.get("content", None)
    if not (title and content):
        flash("Please enter all of the fields", "alert-danger")
        return redirect(url_for('update_post', post_id=post_id, value="Update Post"))

    posts[post_id] = (title, content)
    flash("Your post has successfully been updated", "alert-success")
    return redirect(url_for("get_post", post_id=post_id))
    


@app.route("/posts/<int:post_id>/delete", methods=['GET', 'POST'])
# DELETE POST
def delete_post(post_id):
    if request.method == 'GET':
        post = posts.get(post_id, None)
        if post is None:
            return redirect(url_for("get_all_posts"))
        
        return render_template("delete.html", post_id=post_id, post_title=post[0], post_content=post[1])


    del posts[post_id]
    return redirect(url_for("get_all_posts"))


# CRUD:
# Create
# Read
# Update
# Delete
# HTTP RESPONSE CODES
# See: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status#information_responses for all of the response codes