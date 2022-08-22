# IMPORTS #
# flask imports
from flask import Flask, abort, flash, redirect, request, url_for, render_template
from .db import db  # importing database(db)
from .modals import Post, Reply  # importing modals
from .posts import posts  # importing blueprint from posts.py
# APP & DB
app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile("config.py")
db.init_app(app)

# REGISTER BLUEPRINTS #
app.register_blueprint(posts)

# CRUD #
# Create
# Read
# Update
# Delete
# HTTP RESPONSE CODES #
# See: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status#information_responses for all of the response codes
