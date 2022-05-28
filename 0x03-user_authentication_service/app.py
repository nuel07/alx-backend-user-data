#!/usr/bin/env python3
"""Basic Flask app"""

from flask import Flask, jsonify, request, abort, redirect
from auth import Auth

app = Flask(__name__)
app.url_map.strict_slashes = False
AUTH = Auth()


@app.route('/', methods=['GET'])
def hello():
    """return JSON payload"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users() -> str:
    """get user object"""
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except Exception:
        return jsonify({"message": "email already registered"}), 400
    abort(400)


@app.route('/sessions', methods=['POST'])
def login() -> str:
    """login session"""
    email = request.form.get('email')
    password = request.form.get('password')
    logged = AUTH.valid_login(email, password)
    if logged:
        session_id = AUTH.create_session(email)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie("session_id", session_id)
        return response
    else:
        abort(401)


@app.route('/sessions', methods=['DELETE'])
def logout() -> str:
    """find user by session_id
    and destroy the session"""
    session_cookie = request.cookies.get('session_id')
    the_user = AUTH.get_user_from_session_id(session_cookie)
    if not the_user:
        abort(403)
    AUTH.destroy_session(user_id)
    return redirect('/')


@app.route('/profile', methods=['GET'])
def profile() -> str:
    """find user"""
    user_cookie = request.cookies.get('session_id')
    the_user = AUTH.get_user_from_session_id(user_cookie)
    if the_user:
        return jsonify({"email": the_user.email}), 200
    abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
