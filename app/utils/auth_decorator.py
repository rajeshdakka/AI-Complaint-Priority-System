import jwt
import os
from functools import wraps
from flask import request, redirect


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get("token")

        if not token:
            return redirect("/login-form")

        try:
            data = jwt.decode(
                token,
                os.getenv("SECRET_KEY"),
                algorithms=["HS256"]
            )

            request.user_id = data["user_id"]
            request.role = data["role"]

        except:
            return redirect("/login-form")

        return f(*args, **kwargs)

    return decorated