#!/usr/bin/python3
"""this script contains the first route to the api"""
from flask import Flask, jsonify
app = Flask(__name__)
from models import storage
from api.v1.views import app_views
from os import getenv
app.register_blueprint(app_views)


@app.teardown_appcontext
def reload(exception):
    """reloads all objects from the db"""
    storage.close()

@app.errorhandler(404)
def err_handler(error):
    """handles the 404 errors generated from trying to access
        a resource that does not exist"""
    res = {}
    res['error'] = 'Not found'
    return jsonify(res), 404

if __name__ == "__main__":
    if getenv("HBNB_API_HOST") is None:
        host = '0.0.0.0'
    else:
        host = getenv("HBNB_API_HOST")
    if getenv("HBNB_API_PORT") is None:
        port = 5000
    else:
        port = getenv("HBNB_API_PORT")
    app.run(host=host, port=port, threaded=True)
