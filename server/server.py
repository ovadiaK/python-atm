import http

from flask import Flask, make_response

app = Flask(__name__)


@app.route("/health")
def health():
    resp = make_response("pong", 200)
    return resp


if __name__ == "__main__":
    app.run(debug=True)


def start():
    return "OK"


def endpoint():
    return "200"
