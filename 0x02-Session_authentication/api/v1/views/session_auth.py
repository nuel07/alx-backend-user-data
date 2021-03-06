#!/usr/bin/env python3
""" Session authenticatiion views """
from api.v1.views import app_views
import os
from flask import abort, request, jsonify
from models.user import User


@app_views.route('/auth_session/login/',
                 methods=['POST'], strict_slashes=False)
def login():
    """ returns json representation of all users logged in"""
    email = request.form.get("email")
    password = request.form.get("password")
    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400
    my_users = User.search({"email": email})

    if not my_users:
        return jsonify(error="no user found for this email"), 404

    for user in my_users:
        if not user.is_valid_password(password):
            return jsonify({"error": "wrong password"}), 401
        else:
            from api.v1.app import auth
            sesion_id = auth.create_session(user.id)
            sesion_name = os.getenv("SESSION_NAME")
            users = jsonify(user.to_json())
            users.set_cookie(sesion_name, sesion_id)
            return users


@app_views.route('/auth_session/logout/',
                 methods=['DELETE'], strict_slashes=False)
def logout():
    """ user logout """
    from api.v1.app import auth
    destroy_session = auth.destroy_session(request)
    if destroy_session:
        return jsonify({}), 200
    abort(404)
