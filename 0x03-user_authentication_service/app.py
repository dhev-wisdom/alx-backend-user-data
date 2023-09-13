#!/usr/bin/env python3
"""
Basic Flask App
"""

from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    """home route"""
    res = {"message": "Bienvenue"}
    return jsonify(res)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
