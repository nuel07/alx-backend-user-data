#!/usr/bin/env python3
""" Basic Authentication module """

import base64
from api.v1.auth.auth import Auth
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """ Basic Authentication class """
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """returns the Base64 part of the Authorization
        header for a Basic Authentication
        """
        if authorization_header is None:
            return None
        if type(authorization_header) != str:
            return None
        if authorization_header.startswith("Basic "):
            return "".join(authorization_header.split(" ")[1:])

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """returns the decoded value of a Base64
        string base64_authorization_header
        """
        if base64_authorization_header and type(
                    base64_authorization_header) == str:
            try:
                encded = base64_authorization_header.encode('utf-8')
                dcded = base64.b64decode(encded)
                return dcded.decode('utf-8')
            except Exception:
                return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        ''' returns the user email and the password '''
        creds = decoded_base64_authorization_header
        if creds and type(creds) == str and ":" in creds:
            usr_email = creds.split(':')[0]
            usr_passwd = "".join(creds.split(':', 1)[1:])
            return(usr_email, usr_passwd)
        return(None, None)

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """returns the User instance based
        on his email and password
        """
        if type(user_email) != str:
            return None
        if type(user_pwd) != str:
            return None
        if user_email and user_pwd:
            users = User.search({"email": user_email})
            for user in users:
                if user and user.is_valid_password(user_pwd):
                    return user
        return None
    
    def current_user(self, request=None) -> TypeVar('User'):
        '''retrieves the User instance for a request'''
        if request:
            auth_head = self.authorization_header(request)
            extract = self.extract_base64_authorization_header(auth_head)
            decode = self.decode_base64_authorization_header(extract)
            (email, password) = self.extract_user_credentials(decode)
            return self.user_object_from_credentials(email, password)
