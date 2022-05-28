#!/usr/bin/env python3
"""
End-to-end integration test
"""
import requests


def register_user(email: str, password: str) -> None:
    """register new user"""
    resp = requests.post('http://localhost:5000/users',
                        data={'email': email, 'password': password})
    assert resp.status_code == 200
    assert resp.json() == {'email': email, 'message': "user created"}

def log_in_wrong_password(email: str, password: str) -> None:
    """tests login with wrong password"""
    resp = requests.post('http://localhost:5000/sessions',
                        data={"email": email, "password": password})
    assert resp.status_code == 401

def log_in(email: str, password: str) -> str:
    """tests login with right password"""
    resp = requests.post('http://localhost:5000/sessions',
                        data={"email": email, "password": password})
    assert resp.status_code == 200
    assert resp.json() == {'email': email, 'message': 'logged in'}
    return resp.cookies.get('session_id')

def profile_unlogged() -> None:
    """tests invalidity of session_id"""
    resp = requests.get('http://localhost:5000/profile')
    assert resp.status_code == 403

def profile_logged(session_id: str) -> None:
    """tests validity of session_id"""
    resp = requests.get('http://localhost:5000/profile',
                       cookies={'session_id': session_id})
    assert resp.status_code == 200
    assert resp.json() == {'email': "guillaume@holberton.io"}

def log_out(session_id: str) -> None:
    """test session logout"""
    resp = requests.delete('http://localhost:5000/sessions',
                           cookies={'session_id': session_id})
    for res in resp.history:
        assert res.status_code == 302

def reset_password_token(email: str) -> str:
    """test password reset_token"""
    resp = requests.post('http://localhost:5000/reset_password',
                        data={"email": email})
    assert resp.status_code == 200
    return resp.json().get('reset_token')

def update_password(email: str, reset_token: str, new_password: str) -> None:
    """test update of password with reset_token"""
    resp = requests.put('http://localhost:5000/reset_password',
                       data={
                           "email": email,
                           "reset_token": reset_token,
                           "new_password": new_password})
    assert resp.status_code == 200
    assert resp.json() == {'email': email, 'message': 'Password updated'}


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
