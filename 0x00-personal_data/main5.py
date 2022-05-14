#!/usr/bin/env python3
"""
Main file for task 5
"""

hash_password = __import__('encrypt_password').hash_password

password = "MyAmazingPassw0rd"
print(hash_password(password))
print(hash_password(password))
