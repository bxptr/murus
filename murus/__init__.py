from murus.config import Config
import murus.token

import functools
import requests
import ssl

from flask import Flask, Blueprint
from flask import request, redirect, current_app

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from werkzeug.exceptions import Unauthorized 
from flask import Response
import logging

blueprint = Blueprint("murus", __name__, url_prefix = "/")

limiter = Limiter(key_func = get_remote_address)

limit = lambda rate: limiter.limit(rate) # shorthand fuck you

def murus(app: Flask, config: Config) -> None:
    app.config["MURUS_CONFIG"] = config

    app.logger.setLevel(config.LOG_LEVEL)

    if config.REQUIRE_CLIENT_CERT:
        app.logger.info("Enabling client-certificate validation (mTLS).")
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        context.verify_mode = ssl.CERT_REQUIRED
        context.load_verify_locations(cafile = config.CA_CERT)
        context.load_cert_chain(certfile = config.SERVER_CERT, keyfile = config.SERVER_KEY)

        app.run = lambda host = "0.0.0.0", port = 5000, debug = False: app._original_run(
            host = host,
            port = port,
            debug = debug,
            ssl_context = context
        )
        if not hasattr(app, "_original_run"):
            app._original_run = app.run
    else:
        app.logger.info("mTLS not required or disabled. Only server-side TLS is enabled if used at all.")

    limiter.init_app(app)
    app.register_blueprint(blueprint)

    @app.after_request
    def security_headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        return response

    app.logger.info("Murus extension initialized successfully!")

def protected(token_func: object, redirect_url: str = "/") -> object:
    def wrapper(f: object) -> object:
        @functools.wraps(f)
        def inner(*args, **kwargs) -> object:
            config = current_app.config["MURUS_CONFIG"]
            try:
                candidate = token_func(0)
                payload = token.verify(config, candidate)
                kwargs["payload"] = payload
            except Unauthorized as e:
                return redirect("/", 401)
            return f(*args, **kwargs)
        inner.__name__ = f.__name__
        return inner
    return wrapper

