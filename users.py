import os
from flask import abort, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from db import db


def login(username, password):
    result = db.session.execute("SELECT password FROM Users WHERE username=(:username)", {"username":username})
    user = result.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session["username"] = username
            session["csrf_token"] = os.urandom(16).hex()
            return True
        else:
            return False

def logout():
    del session["username"]

def register(username, password):
    hash_value = generate_password_hash(password)
    try:
        db.session.execute("""
            INSERT INTO Users (username, password, admin) VALUES (:username,:password, FALSE)""",
            {"username":username, "password":hash_value})
        db.session.commit()
    except:
        return False
    return login(username, password)

def change_password(password, password1):
    username = session["username"]
    result = db.session.execute("SELECT id, password FROM Users WHERE username=(:username)", {"username":username})
    user = result.fetchone()
    if check_password_hash(user.password, password):
        hash_password1 = generate_password_hash(password1)
        db.session.execute("UPDATE Users SET password=(:hash_password1) WHERE username=(:username)", {"hash_password1":hash_password1, "username":username})
        db.session.commit()
        return True
    return False

def admin():
    username = session["username"]
    result = db.session.execute("SELECT admin FROM Users WHERE username=(:username)", {"username":username})
    user = result.fetchone()
    return user.admin

def check_csrf():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
