import os

from flask import Flask, make_response


def create_app():
    # create and configure the app
    app = Flask(__name__)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/health")
    def health():
        resp = make_response("pong", 200)
        return resp

    @app.route("/fill", methods=['POST'])
    def fill():
        print("money in")

    @app.route("/withdraw", methods=['PUT'])
    def withdraw():
        print("money out")

    return app
