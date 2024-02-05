#!/usr/bin/python3
"""this script contains the reload and errorhandler functions
    also contains the app instance and uses CORS"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS


# creating an app instance which will be used to run the site
app = Flask(__name__)


# registering a blueprint which will be used in the files in views folder
app.register_blueprint(app_views)
CORS(app, resources={r"/api/*": {"origins": '0.0.0.0'}})


# the teardown function which is executed after every request
@app.teardown_appcontext
def reload(exception):
    """reloads all objects from the db useful when a change is made
        after the reuest all objects are reloaded"""
    storage.close()


# the function that handles the 404 error if it occurs
@app.errorhandler(404)
def err_handler(error):
    """handles the 404 errors generated from trying to access
        a resource that does not exist"""
    res = {}
    res['error'] = 'Not found'
    return jsonify(res), 404


# running the app only if the module is not imported in another module
if __name__ == "__main__":
    """the function will only execute if the module is run from here
        and not if imported"""
    HOST = getenv("HBNB_API_HOST", '0.0.0.0')
    PORT = int(getenv("HBNB_API_PORT", 5000))
    app.run(host=HOST, port=PORT, threaded=True)
