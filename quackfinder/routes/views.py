from flask import Blueprint, render_template, request

main = Blueprint("main", __name__)

#Main page and route request handler.
@main.route("/", methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        pass
       
    return render_template("index.html")

#Add points to map by handling json requests
@main.post("/points")
def add_point():
    pass