import jwt
import sqlite3
import time
import os


EXPIRE = time
SECRET_KEY = os.getenv('JWT_SECRET_KEY')


def validate(key):
    payload = {}
    access_token = jwt.encode(
        payload,
        algorithm='HS256',
        key=SECRET_KEY
    )
    return access_token
