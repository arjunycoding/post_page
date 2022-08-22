# IMPORTS #
# importing all of the flask stuff
from flask import Blueprint, Flask, flash, redirect, request, url_for, render_template
from .db import db  # importing database(db)
from .modals import Post, Reply  # importing modals

# BLUEPRINTS #
posts = Blueprint(
    "posts",
    __name__
)

# ALL ROUTES #


@posts.route("/")
# ALL POSTS #
def get_all():
    limit = request.args.get("limit", 5, type=int)
    offset = request.args.get("offset", 0, type=int)
    max = len(Post.query.order_by(Post.id).all()) - 5
    if max % 5 != 0:
        while max % 5 != 0:
            max += 1
    posts = Post.query.order_by(Post.id).limit(limit).offset(offset).all()
    print(max)
    return render_template(
        "all.html",
        posts=posts,
        max=max,
        offset=offset,
        limit=limit
    )


@posts.route("/<int:post_id>")
# VIEW SPECIFIC POST #
def get(post_id):
    post = Post.query.get(post_id)
    print(post)
    if post == None:
        return render_template("all.html", posts=Post.query.all())
    return render_template(
        "get.html",
        post_title=post.title,
        post_content=post.content,
        post_id=post_id
    )


@posts.route("/new", methods=['GET', 'POST'])
# NEW POST #
def new():
    if request.method == 'GET':
        return render_template("new.html")
    title = request.form.get("title", None)
    content = request.form.get("content", None)
    if not (title and content):
        flash("Please enter all of the fields", "alert-danger")
        return redirect(url_for('posts.new'))

    post = Post(title=title, content=content)
    db.session.add(post)
    db.session.commit()
    flash("Your post has successfully been created", "alert-success")
    return redirect(url_for("posts.get_all", posts=Post.query.all()))


@posts.route("/<int:post_id>/update", methods=['GET', 'POST'])
# UPDATE POST  #
def update(post_id):
    if request.method == 'GET':
        post = Post.query.get(post_id)

        if post == None:
            return redirect(url_for("posts.get_all", posts=Post.query.all()))

        return render_template(
            "new.html",
            post_title=post.title,
            post_content=post.content,
            value="Update Post",
            title="Update Post"
        )

    title = request.form.get("title", None)
    content = request.form.get("content", None)
    if not (title and content):
        flash("Please enter all of the fields", "alert-danger")
        return redirect(url_for('posts.update', post_id=post.id, value="Update Post"))

    post = Post.query.get(post_id)
    post.title = title
    post.content = content

    db.session.commit()

    flash("Your post has successfully been updated", "alert-success")
    return redirect(url_for("posts.get", post_id=post.id))


@posts.route("/<int:post_id>/delete", methods=['GET', 'POST'])
# DELETE POST #
def delete(post_id):
    if request.method == 'GET':
        post = Post.query.get(post_id)
        if post is None:
            return redirect(url_for("posts.get_all"))

        return render_template(
            "delete.html",
            post_id=post_id,
            post_title=post.title,
            post_content=post.content)

    post = Post.query.get(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for("posts.get_all"))
