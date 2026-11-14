from flask import Flask
from quackfinder.routes.views import main

#Create flask app based off of main template in views
def create_app():
    app = Flask(__name__)
    app.register_blueprint(main)

    return app