#!/usr/bin/env python3
"""
Basic Flask App
"""

from flask import Flask, jsonify, request, abort
from auth import Auth, _hash_password
from sqlalchemy.exc import NoResultFound
from user import User

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
            return jsonify(res), status_code

@app.route("/sessions", strict_slashes=False, methods=["POST"])
def login():
    """login function"""
    email = request.form.get("email")
    password = request.form.get("password")
    
    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie("session_id", session_id)
        return response
    else:
        abort(401)
    


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
