from murus.config import Config

import jwt
import datetime
from flask import request
from werkzeug.exceptions import Unauthorized

def create(config: Config, user_id: str, additional_claims: dict = None) -> str:
    if additional_claims is None:
        additional_claims = {}
    payload = {
        "sub": user_id,
        "iat": datetime.datetime.utcnow(),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds = config.JWT_EXPIRATION_DELTA_SECONDS),
    }
    payload.update(additional_claims)
    token = jwt.encode(payload, config.JWT_SECRET_KEY, algorithm = config.JWT_ALGORITHM)
    return token

def verify(config: Config, token: str) -> dict:
    try:
        payload = jwt.decode(token, config.JWT_SECRET_KEY, algorithms = [config.JWT_ALGORITHM])
        return payload
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError) as e:
        raise Unauthorized(str(e))

def extract(config: Config, token: str) -> dict:
    try:
        payload = jwt.decode(token, config.JWT_SECRET_KEY, algorithms = [config.JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise Unauthorized("Token has expired.")
    except jwt.InvalidTokenError as e:
        raise Unauthorized(f"Invalid token: {str(e)}")

