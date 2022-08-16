# IMPORTS
from flask import Flask, request, url_for, render_template

# VARIABLES
app = Flask(__name__)

#  Home Page
@app.route("/")
def index():
    return render_template("index.html", title="Home")

# Greeting Page
@app.route("/greet/<name>")
def hello_name(name):
    return render_template("greet.html", name=name, title="Hello")

# Addition Calculator
@app.route("/addition", methods=["POST", "GET"])
def add():
    result = None
    if request.method == "POST":
        a = request.form.get("a", 0,  type=int)
        b = request.form.get("b", 0,  type=int)
        result = (a, b, a+b)
    return render_template("add.html", result=result) 