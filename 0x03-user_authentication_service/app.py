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
    if the_user:
        AUTH.destroy_session(the_user.id)
        return redirect('/')
    else:
        abort(403)


@app.route('/profile', methods=['GET'])
def profile() -> str:
    """find user"""
    user_cookie = request.cookies.get('session_id')
    the_user = AUTH.get_user_from_session_id(user_cookie)
    if the_user:
        return jsonify({"email": the_user.email}), 200
    abort(403)


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token() -> str:
    email = request.form.get('email')
    try:
        rset_token = AUTH.get_reset_password_token(email)
        if rset_token:
            return jsonify({"email": email, "reset_token": rset_token}), 200
        else:
            abort(403)
    except ValueError:
        abort(403)


@app.route('/reset_password', methods=['PUT'])
def update_password() -> str:
    """update password endpoint"""
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except Exception:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
