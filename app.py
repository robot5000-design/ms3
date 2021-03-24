import os
import requests
import datetime
import math
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from flask_talisman import Talisman
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY")
app.api_key = os.environ.get("API_KEY")
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")

csp = {
    'default-src': '\'self\'',
    'script-src': [
        '\'self\'',
        'code.jquery.com',
        'cdn.jsdelivr.net',
        'cdnjs.cloudflare.com'
    ],
    'font-src': '\'self\' themes.googleusercontent.com *.gstatic.com',
    'style-src': [
        '\'self\' ajax.googleapis.com fonts.googleapis.com'
        '*.gstatic.com',
        'code.jquery.com',
        'cdn.jsdelivr.net',
        'cdnjs.cloudflare.com'
    ],
    'img-src': [
        '\'self\'',
        'image.tmdb.org'
    ],
    'media-src': [
        '\'self\'',
        'api.themoviedb.org'
    ]
}
'''talisman = Talisman(
    app,
    content_security_policy=csp,
    content_security_policy_nonce_in=['script-src']
)'''

mongo = PyMongo(app)


@app.route('/')
@app.route('/index')
def index():
    movie_details = mongo.db.movie_details.find().sort(
        "last_review_date", -1).limit(10)
    if movie_details:
        tmdb_poster_url = mongo.db.tmdb_urls.find_one()["tmdb_poster_url"]
        return render_template("index.html", movie_details=movie_details,
                               tmdb_poster_url=tmdb_poster_url)
    return render_template("index.html")


@app.route("/browse_reviews/<sort_by>/<int:page>")
@app.route("/browse_reviews", defaults={'sort_by': 'latest', 'page': 0})
def browse_reviews(sort_by, page):
    review_count = mongo.db.movie_details.find().count()
    total_pages = math.ceil(review_count / 12)
    if sort_by == "latest":
        movie_details = mongo.db.movie_details.find().sort(
            "last_review_date", -1).skip(page * 12).limit(12)
    elif sort_by == "rating":
        movie_details = mongo.db.movie_details.find().sort(
            "overall_rating", -1).skip(page * 12).limit(12)
    elif sort_by == "popularity":
        movie_details = mongo.db.movie_details.find().sort(
            "number_reviews", -1).skip(page * 12).limit(12)
    if movie_details:
        tmdb_poster_url = mongo.db.tmdb_urls.find_one()["tmdb_poster_url"]
        return render_template("reviews.html", movie_details=movie_details,
                               tmdb_poster_url=tmdb_poster_url,
                               sort_by=sort_by, page=page,
                               review_count=review_count,
                               total_pages=total_pages)
    return render_template("reviews.html")


@app.route("/my_reviews/<sort_by>/<int:page>")
@app.route("/my_reviews", defaults={'sort_by': 'latest', 'page': 0})
def my_reviews(sort_by, page):
    if sort_by == "latest":
        my_reviews = list(mongo.db.reviews.find({"created_by": session[
            "user"]}).sort("review_date", -1).skip(page * 6).limit(6))
    elif sort_by == "oldest":
        my_reviews = list(mongo.db.reviews.find({"created_by": session[
            "user"]}).sort("review_date", 1).skip(page * 6).limit(6))
    movie_id_list = []
    for review in my_reviews:
        movie_id_list.append(review["tmdb_id"])
    review_count = len(my_reviews)
    total_pages = math.ceil(review_count / 6)
    # pick out the movies details that we need
    movie_details = []
    index = page * 6
    while index < len(movie_id_list):
        movie_detail = list(mongo.db.movie_details.find(
            {"tmdb_id": movie_id_list[index]}))
        movie_details.extend(movie_detail)
        index += 1
    if movie_details:
        tmdb_poster_url = mongo.db.tmdb_urls.find_one()["tmdb_poster_url"]
    return render_template("my_reviews.html", movie_details=movie_details,
                           tmdb_poster_url=tmdb_poster_url,
                           page=page,
                           review_count=review_count,
                           total_pages=total_pages)
    #return render_template("my_reviews.html")


@app.route('/review_detail/<tmdb_id>')
def review_detail(tmdb_id):
    reviews = list(mongo.db.reviews.find(
        {"tmdb_id": tmdb_id}).sort("review_date", -1))
    movie_detail = list(mongo.db.movie_details.find(
        {"tmdb_id": tmdb_id}))
    if "user" in session:
        already_reviewed = list(mongo.db.reviews.find({"tmdb_id": tmdb_id,
                                "created_by": session["user"]}))
    else:
        already_reviewed = False
    tmdb_poster_url = mongo.db.tmdb_urls.find_one()["tmdb_poster_url"]
    for review in reviews:
        review["review_date"] = review["review_date"].strftime("%d-%m-%Y")
    overall_rating = 0
    for review in reviews:
        overall_rating += int(review["rating"])
    session["overall_rating"] = overall_rating
    try:
        overall_rating = round((overall_rating / len(reviews)), 2)
    except ZeroDivisionError:
        flash("Oops we have a zero division error")
    if reviews:
        return render_template("review_detail.html", reviews=reviews,
                               movie_detail=movie_detail[0],
                               tmdb_poster_url=tmdb_poster_url,
                               overall_rating=overall_rating,
                               already_reviewed=already_reviewed)
    else:
        return redirect(url_for("index.html"))


@app.route("/search/<int:page_number>", methods=["GET", "POST"])
def search_movies(page_number):
    if request.method == "POST":
        session["search"] = True
        session["search_query"] = request.form.get("query")
        session["media_type"] = request.form.get("media_type")
        return api_request(page_number)
    session.pop("search_query", None)
    session.pop("media_type", None)
    return render_template("search.html")


@app.route("/search_pagination/<int:page_number>")
def search_pagination(page_number):
    flash("Page " + str(page_number))
    if "search_query" in session:
        return api_request(page_number)
    else:
        return redirect(url_for("search_movies", page_number=1))


def api_request(page_number):
    search_url_movie = mongo.db.tmdb_urls.find()[0]['search_url_movie'].format(
        app.api_key, page_number, session['search_query'])
    search_url_tv = mongo.db.tmdb_urls.find()[0]['search_url_tv'].format(
        app.api_key, page_number, session['search_query'])
    if session["media_type"] == "tv":
        search_url = search_url_tv
    else:
        search_url = search_url_movie
    try:
        api_request = requests.get(search_url)
    except requests.exceptions.ConnectionError:
        flash("Cannot get results from the database\
                at this time. Please try again later.")
    else:
        if api_request.status_code == 200:
            search_results = api_request.json()
            if "results" in search_results:
                return render_template(
                    "search.html", search_results=search_results)
            else:
                flash("There's been a problem. Please try again later.")
        else:
            flash("Status " + str(api_request.status_code) + " " + api_request.reason + ". Cannot get results \
                from the database at this time. Please try again later.")


@app.route("/new_review/<tmdb_id>/<media_type>/<page_number>",
           methods=["GET", "POST"])
def new_review(tmdb_id, media_type, page_number):
    if request.method == "POST":
        # check if movie details already exist in db and if not, add them
        details_exist = mongo.db.movie_details.find_one(
            {"tmdb_id": session["selected_media"]["tmdb_id"]})
        if not details_exist:
            session["selected_media"]["overall_rating"] = int(request.form.get(
                "inlineRadioOptions"))
            session["selected_media"]["number_reviews"] = 1
            mongo.db.movie_details.insert_one(dict(session["selected_media"]))
        else:
            # update overall rating and number of reviews for sorting purposes
            total_rating = session["overall_rating"] + int(
                request.form.get("inlineRadioOptions"))
            number_reviews = details_exist["number_reviews"] + 1
            update_rating = total_rating / number_reviews
            mongo.db.movie_details.update_one(
                {"tmdb_id": session["selected_media"]["tmdb_id"]},
                {"$set": {"overall_rating": round(float(update_rating), 2)}})
            mongo.db.movie_details.update_one(
                {"tmdb_id": session["selected_media"]["tmdb_id"]},
                {"$set": {"number_reviews": int(
                    details_exist["number_reviews"] + 1)}})
            mongo.db.movie_details.update_one(
                {"tmdb_id": session["selected_media"]["tmdb_id"]},
                {"$set": {"last_review_date": datetime.datetime.now()}})
        # Add new review to db
        new_review = {
            "tmdb_id": str(session["selected_media"]["tmdb_id"]),
            "genre": request.form.get("select-genre"),
            "review": request.form.get("review-text"),
            "rating": request.form.get("inlineRadioOptions"),
            "review_date": datetime.datetime.now(),
            "created_by": session["user"]
        }
        mongo.db.reviews.insert_one(new_review)
        session.pop("selected_media")
        session.pop("search_query", None)
        session.pop("media_type", None)
        session.pop("overall_rating", None)
        flash("Review Posted Successfully!")
        return redirect(url_for("browse_reviews"))
    media_detail = get_choice_detail(tmdb_id, media_type)
    already_reviewed = list(mongo.db.reviews.find({"tmdb_id": tmdb_id,
                            "created_by": session["user"]}))
    if "status_code" in media_detail:
        if media_detail["status_code"] == 34:
            flash("Sorry. This resource cannot be found.")
            return redirect(url_for("search_movies", page_number=page_number))
    else:
        validate_choice(media_detail)
        genres = mongo.db.genres.find().sort("genre_name", 1)
        tmdb_poster_url = mongo.db.tmdb_urls.find_one()["tmdb_poster_url"]
        return render_template(
            "new_review.html", media_detail=session["selected_media"],
            page_number=page_number,
            genres=genres,
            tmdb_poster_url=tmdb_poster_url,
            already_reviewed=already_reviewed)


def get_choice_detail(tmdb_id, media_type):
    tv_detail_url = mongo.db.tmdb_urls.find()[0]['tv_detail_url'].format(
        tmdb_id, app.api_key)
    movie_detail_url = mongo.db.tmdb_urls.find()[0]['movie_detail_url'].format(
        tmdb_id, app.api_key)
    session["media_type"] = media_type
    if media_type == "tv":
        detail_url = tv_detail_url
    else:
        detail_url = movie_detail_url
    try:
        detail_request = requests.get(detail_url)
    except requests.exceptions.ConnectionError:
        flash("Cannot get results from the database\
                at this time. Please try again later.")
    else:
        if detail_request.status_code == 200:
            media_detail = detail_request.json()
            if "id" in media_detail:
                return media_detail
            else:
                flash("There's been a problem. Please try again later.")
        else:
            flash("Status " + str(detail_request.status_code) + " " + detail_request.reason + ". Cannot get results \
                from the database at this time. Please try again later.")


def validate_choice(media_detail):
    session["selected_media"] = {}
    if "id" in media_detail:
        session["selected_media"]["tmdb_id"] = str(media_detail["id"])
    if "original_title" in media_detail:
        session["selected_media"][
            "original_title"] = media_detail["original_title"]
    elif "original_name" in media_detail:
        session["selected_media"][
            "original_title"] = media_detail["original_name"]
    session["selected_media"]["media_type"] = session["media_type"]
    if "first_air_date" in media_detail:
        if media_detail["first_air_date"] is None or media_detail[
                "first_air_date"] == "":
            session["selected_media"]["release_date"] = ""
        else:
            session["selected_media"][
                "release_date"] = media_detail["first_air_date"][0:4]
    elif "release_date" in media_detail:
        if media_detail["release_date"] is None or media_detail[
                "release_date"] == "":
            session["selected_media"]["release_date"] = ""
        else:
            session["selected_media"][
                "release_date"] = media_detail["release_date"][0:4]
    else:
        session["selected_media"]["release_date"] = ""
    if "poster_path" in media_detail:
        if media_detail["poster_path"] == "" or media_detail[
                "poster_path"] is None:
            session["selected_media"]["poster_path"] = None
        else:
            session["selected_media"][
                "poster_path"] = media_detail["poster_path"]
    if "overview" in media_detail:
        session["selected_media"]["overview"] = media_detail["overview"]
    else:
        session["selected_media"]["overview"] = None
    session["selected_media"]["last_review_date"] = datetime.datetime.now()


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username exists in db
        username = request.form.get("username")
        existing_user = mongo.db.users.find_one(
            {"username": username.lower()})
        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                session["user"] = username.lower()
                flash(f"Welcome, {username}")
                return redirect(url_for("index"))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("index"))
        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("index"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username2")
        # check if username already exists in db
        existing_user = mongo.db.users.find_one(
            {"username": username.lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("index"))

        password1 = request.form.get("password2")
        password2 = request.form.get("confirm-password2")
        if password1 != password2:
            flash("Passwords do not match!")
            return redirect(url_for("index"))

        register = {
            "username": username.lower(),
            "password": generate_password_hash(request.form.get("password2"))
        }
        mongo.db.users.insert_one(register)

        # put the new user into 'session' cookie
        session["user"] = username.lower()
        flash("Registration Successful!")
        return redirect(url_for("index"))
    return render_template("register.html")


@app.route("/logout")
def logout():
    # remove user from session cookie
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
