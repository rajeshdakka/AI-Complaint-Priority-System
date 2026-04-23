# app/routes/auth_routes.py

import jwt
import datetime
import os

from flask import (
    Blueprint,
    request,
    render_template,
    redirect,
    make_response
)

from app.services.db_service import get_db_connection
from app import bcrypt

auth_bp = Blueprint("auth", __name__)


# -----------------------------------
# Home Page
# -----------------------------------
@auth_bp.route("/")
def home():
    return render_template("home.html")


# -----------------------------------
# Register Form Page
# -----------------------------------
@auth_bp.route("/register-form")
def register_form():
    return render_template("register.html")


# -----------------------------------
# Register User
# -----------------------------------
@auth_bp.route("/register", methods=["POST"])
def register():
    try:
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        mobile = request.form["mobile"]

        role = request.form.get("role", "user")

        hashed_pw = bcrypt.generate_password_hash(
            password
        ).decode("utf-8")

        db = get_db_connection()
        cursor = db.cursor()

        cursor.execute("""
            INSERT INTO users
            (name, email, password_hash, role, mobile)
            VALUES (?, ?, ?, ?, ?)
        """, (
            name,
            email,
            hashed_pw,
            role,
            mobile
        ))

        db.commit()
        cursor.close()
        db.close()

        return redirect("/login-form")

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }, 500


# -----------------------------------
# Login Form Page
# -----------------------------------
@auth_bp.route("/login-form")
def login_form():
    return render_template("login.html")


# -----------------------------------
# Login User
# -----------------------------------
@auth_bp.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        return "Email and password required", 400

    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("""
        SELECT id, password_hash, role
        FROM users
        WHERE email=?
    """, (email,))

    result = cursor.fetchone()

    if not result:
        cursor.close()
        db.close()
        return "User not found", 404

    user_id = result["id"]
    stored_hash = result["password_hash"]
    role = result["role"]

    if not bcrypt.check_password_hash(
        stored_hash,
        password
    ):
        cursor.close()
        db.close()
        return "Invalid password", 401

    cursor.close()
    db.close()

    token = jwt.encode(
        {
            "user_id": user_id,
            "role": role,
            "exp": datetime.datetime.utcnow()
                   + datetime.timedelta(hours=2)
        },
        os.getenv("SECRET_KEY"),
        algorithm="HS256"
    )

    if isinstance(token, bytes):
        token = token.decode("utf-8")

    response = make_response(
        redirect("/reports")
    )

    response.set_cookie(
        "token",
        token,
        httponly=True,
        samesite="Lax",
        path="/"
    )

    return response


# -----------------------------------
# Logout
# -----------------------------------
@auth_bp.route("/logout")
def logout():
    response = make_response(
        redirect("/login-form")
    )

    response.delete_cookie(
        "token",
        path="/"
    )

    return response