#!/usr/bin/env python3
"""
Module documentation
"""

import requests


def register_user(email: str, password: str) -> None:
    """querry route to register user"""
    url = "http://127.0.0.1:5000/users"
    payload = {"email": email, "password": password}
    res = requests.post(url, payload)
    assert res.status_code == 200


def log_in_wrong_password(email: str, password: str) -> None:
    """wrong password login"""
    url = "http://127.0.0.1:5000/sessions"
    payload = {"email": email, "password": password}
    res = requests.post(url, payload)
    assert res.status_code == 401


def log_in(email: str, password: str) -> str:
    """login"""
    url = "http://127.0.0.1:5000/sessions"
    payload = {"email": email, "password": password}
    res = requests.post(url, payload)
    assert res.status_code == 200
    return res.cookies.get("session_id")


def profile_unlogged() -> None:
    """try to access profile when user not logged in"""
    url = "http://127.0.0.1:5000/profile"
    res = requests.get(url)
    assert res.status_code == 403


def profile_logged(session_id: str) -> None:
    """try to access profile when user not logged in"""
    url = "http://127.0.0.1:5000/profile"
    res = requests.get(url, cookies={"session_id": session_id})
    assert res.status_code == 200


def log_out(session_id: str) -> None:
    """logout"""
    url = "http://127.0.0.1:5000/sessions"
    res = requests.delete(url, cookies={"session_id": session_id})
    assert res.status_code == 200


def reset_password_token(email: str) -> str:
    """reset password"""
    url = "http://127.0.0.1:5000/reset_password"
    payload = {"email": email}
    res = requests.post(url, payload)
    assert res.status_code == 200
    return res.json().get("reset_token")


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """reset password"""
    url = "http://127.0.0.1:5000/reset_password"
    payload = {"email": email, "reset_token": reset_token,
               "new_password": new_password}
    res = requests.put(url, payload)
    assert res.status_code == 200


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
