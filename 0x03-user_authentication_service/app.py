#!/usr/bin/env python3
"""
Basic Flask App
"""

from flask import Flask, jsonify, request, abort, redirect, url_for
from auth import Auth, _hash_password
from db import DB
from sqlalchemy.exc import NoResultFound
from user import User
import uuid

AUTH = Auth()
DB = DB()

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


@app.route("/sessions", strict_slashes=False, methods=["DELETE"])
def logout():
    """
    logout function
    destroy session
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect(url_for('home'))
    abort(403)


@app.route("/profile", strict_slashes=False, methods=["GET"])
def profile():
    """
    check if user exists (by session id) and return user email
    """
    session_id = request.cookies.get("session_id")
    if not session_id:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        response = {"email": user.email}
        return jsonify(response), 200
    abort(403)


@app.route("/reset_password", strict_slashes=False, methods=["POST"])
def get_reset_password_token():
    """
    get reset password token
    """
    email = request.form.get("email")
    try:
        reset_token = AUTH.generate_reset_password_token(email)
        if not reset_token:
            abort(403)
        response = {"email": email, "reset_token": reset_token}
        return jsonify(response), 200
    except ValueError:
        abort(403)


@app.route("/reset_password", strict_slashes=False, methods=["PUT"])
def update_password():
    """
    update user password
    """
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    password = request.form.get("new_password")
    try:
        AUTH.update_password(reset_token, password)
        response = {"email": email, "message": "Password updated"}
        return jsonify(response), 200
    except Exception as e:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
