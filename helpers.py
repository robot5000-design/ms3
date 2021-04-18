import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from flask_talisman import Talisman
from flask_wtf.csrf import CSRFProtect
from flask_wtf.csrf import CSRFError
if os.path.exists("env.py"):
    import env

app = Flask(__name__)

# Configuration settimgs
app.secret_key = os.environ.get("SECRET_KEY")
app.api_key = os.environ.get("API_KEY")
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
)

# Talisman CSP settings
csp = {
    'default-src': [
        '\'none\''
    ],
    'script-src': [
        '\'strict-dynamic\'',
        '\'unsafe-inline\'',
        'code.jquery.com',
        'cdn.jsdelivr.net',
        'cdnjs.cloudflare.com',
        'api.emailjs.com'
    ],
    'font-src': [
        '\'self\'',
        'themes.googleusercontent.com *.gstatic.com',
        'fonts.googleapis.com',
        'cdnjs.cloudflare.com'
    ],
    'style-src': [
        '\'self\'',
        'cdn.jsdelivr.net',
        'cdnjs.cloudflare.com',
        'fonts.googleapis.com'
    ],
    'img-src': [
        '\'self\'',
        'image.tmdb.org',
        'data:'
    ],
    'connect-src': [
        '\'self\'',
        'api.emailjs.com'
    ],
    'object-src': [
        '\'none\''
    ],
    'frame-src': [
        'cdn.jsdelivr.net'
    ],
    'base-uri': [
        '\'none\''
    ],
    'frame-ancestors': [
        '\'none\''
    ]
}

# Applies Talisman CSP protection to the app
talisman = Talisman(app,
                    force_https=True,
                    content_security_policy_nonce_in=['script-src'],
                    content_security_policy=csp)

# Applies CSRF protection for all forms
csrf = CSRFProtect(app)

mongo = PyMongo(app)


def block_users():
    """ Blocks users from using the site.

    Gets values from the block_selected form. Validates that the
    list returned has entries and that the user is not already blocked
    and inserts them in the blocked_users collection in the database.
    """
    block_list_users = request.form.getlist("block-selected")
    if len(block_list_users) != 0:
        for user in block_list_users:
            already_blocked = mongo.db.blocked_users.find_one(
                {"username": user})
            if already_blocked:
                flash("User(s) Already Blocked")
            else:
                mongo.db.blocked_users.insert_one(
                    {"username": user})
        flash("User(s) Blocked")


def unblock_users():
    """ Unblocks users from using the site.

    Requests values from the unblock_selected form. Validates that the
    list returned has entries and removes them from the blocked_users
    collection in the database.
    """
    unblock_list_users = request.form.getlist("unblock-selected")
    if len(unblock_list_users) != 0:
        for user in unblock_list_users:
            mongo.db.blocked_users.delete_one(
                {"username": user})
        flash("User(s) Unblocked")
