#!/usr/bin/env python3
"""
Basic Flask App
"""

from flask import Flask, jsonify, request, make_response
from auth import Auth

AUTH = Auth()

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    """home route"""
    res = {"message": "Bienvenue"}
    return jsonify(res)


@app.route("/users", strict_slashes=False, methods=["POST"])
def users():
    """
    register user with passed data
    """
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        try:
            user = AUTH.register_user(email=email, password=password)
            return jsonify({"email": email, "message": "user created"})
        except ValueError:
            res = {"message": "email already registered"}
            status_code = 400
            response = make_response(res, status_code)
            return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
