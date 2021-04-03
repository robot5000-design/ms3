import os
import datetime
import math
import requests
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from flask_talisman import Talisman
from flask_wtf.csrf import CSRFProtect
from flask_wtf.csrf import CSRFError
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY")
app.api_key = os.environ.get("API_KEY")
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")

csp = {
    'default-src': [
        '\'self\'',
        'https:',
        'none'
    ],
    'script-src': [
        '\'self\'',
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
        'code.jquery.com',
        'cdn.jsdelivr.net',
        'cdnjs.cloudflare.com',
        'fonts.googleapis.com'
    ],
    'img-src': [
        '\'self\'',
        'image.tmdb.org',
        'data:'
    ]
}

talisman = Talisman(app, content_security_policy=csp)

app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
)

mongo = PyMongo(app)
csrf = CSRFProtect(app)


@app.route('/', methods=["GET", "POST"])
@app.route('/index', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        session["search"] = True
        session["search_query"] = request.form.get("query")
        session["media_type"] = request.form.get("media_type")
        return api_request(page=1)
    movie_details = list(mongo.db.movie_details.find().sort(
        "last_review_date", -1).limit(12))
    if movie_details:
        tmdb_poster_url = mongo.db.tmdb_urls.find_one()["tmdb_poster_url"]
        return render_template("index.html", movie_details=movie_details,
                               tmdb_poster_url=tmdb_poster_url)
    return render_template("index.html")


@app.route("/browse_reviews/<int:page>", methods=[
           "GET", "POST"])
def browse_reviews(page):
    if request.method == "POST":
        query = request.form.get("search-box")
        browse_reviews_sort = request.form.get("browse_reviews_sort")
        if query:
            search_term = {"$text": {"$search": query}}
        else:
            search_term = None
    else:
        search_term = None
        query = ""
        browse_reviews_sort = "latest"
    review_count = mongo.db.movie_details.find(search_term).count()
    total_pages = math.ceil(review_count / 12)
    if browse_reviews_sort == "rating":
        movie_details = list(mongo.db.movie_details.find(search_term).sort(
            "overall_rating", -1).skip(page * 12).limit(12))
    elif browse_reviews_sort == "popularity":
        movie_details = list(mongo.db.movie_details.find(search_term).sort(
            "number_reviews", -1).skip(page * 12).limit(12))
    else:
        movie_details = list(mongo.db.movie_details.find(search_term).sort(
            "last_review_date", -1).skip(page * 12).limit(12))
    if movie_details:
        tmdb_poster_url = mongo.db.tmdb_urls.find_one()["tmdb_poster_url"]
        return render_template("reviews.html", movie_details=movie_details,
                               tmdb_poster_url=tmdb_poster_url,
                               browse_reviews_sort=browse_reviews_sort,
                               page=page,
                               review_count=review_count,
                               total_pages=total_pages,
                               query=query)
    return render_template("reviews.html",
                           browse_reviews_sort=browse_reviews_sort, page=page)


@app.route("/my_reviews/<user>/<my_reviews_sort>/<int:page>", methods=[
           "GET", "POST"])
def my_reviews(user, my_reviews_sort, page):
    if request.method == "POST":
        query = request.form.get("search-box")
        my_reviews_sort = request.form.get("my_reviews_sort")
        if query:
            search_term = {"$text": {"$search": query}, "created_by": user}
        else:
            search_term = {"created_by": user}
    else:
        search_term = {"created_by": user}
        query = ""
    if my_reviews_sort == "alphabetically":
        my_reviews_search = list(mongo.db.reviews.find(search_term).sort(
            "original_title", 1).skip(page * 12).limit(12))
    elif my_reviews_sort == "oldest":
        my_reviews_search = list(mongo.db.reviews.find(search_term).sort(
            "review_date", 1).skip(page * 12).limit(12))
    else:
        my_reviews_sort = "latest"
        my_reviews_search = list(mongo.db.reviews.find(search_term).sort(
            "review_date", -1).skip(page * 12).limit(12))
    if my_reviews_search:
        movie_id_list = []
        for review in my_reviews_search:
            movie_id_list.append(review["tmdb_id"])
        review_count = mongo.db.reviews.find({"created_by": user}).count()
        total_pages = math.ceil(review_count / 12)
        # pick out the movies details that we need
        movie_details = []
        iteration = 0
        while iteration < len(movie_id_list):
            movie_detail = list(mongo.db.movie_details.find(
                {"tmdb_id": movie_id_list[iteration]}))
            movie_details.extend(movie_detail)
            iteration += 1
        if movie_details:
            tmdb_poster_url = mongo.db.tmdb_urls.find_one()["tmdb_poster_url"]
        return render_template("my_reviews.html", movie_details=movie_details,
                               tmdb_poster_url=tmdb_poster_url,
                               page=page, my_reviews_sort=my_reviews_sort,
                               review_count=review_count,
                               total_pages=total_pages,
                               user=user, query=query)
    return render_template("my_reviews.html", user=user,
                           my_reviews_sort=my_reviews_sort, page=page)


@app.route("/delete_review/<tmdb_id>/<user>")
def delete_review(tmdb_id, user):
    if check_user_permission() == "valid-user":
        if user == session["user"] or session["user"] == "admin":
            mongo.db.reviews.delete_one(
                {"tmdb_id": tmdb_id, "created_by": user.lower()})
            flash("Review Successfully Deleted")
            # check if there are other reviews, otherwise delete movie
            # details in the db
            other_reviews = mongo.db.reviews.find_one(
                {"tmdb_id": tmdb_id})
            if not other_reviews:
                mongo.db.movie_details.delete_one(
                    {"tmdb_id": tmdb_id})
            if session["user"] == "admin":
                return redirect(url_for('browse_reviews', page=0))
            return redirect(url_for('my_reviews', user=user,
                                    my_reviews_sort='latest', page=0))
    flash("You do not have permission to access the requested resource")
    return redirect(url_for("index"))


@app.route("/delete_review/<tmdb_id>")
def delete_all(tmdb_id):
    if check_user_permission() == "valid-user":
        if session["user"] == "admin":
            mongo.db.reviews.delete_many(
                {"tmdb_id": tmdb_id})
            mongo.db.movie_details.delete_one(
                {"tmdb_id": tmdb_id})
            flash("Movie & Reviews Successfully Deleted")
            return redirect(url_for('browse_reviews', page=0))
    flash("You do not have permission to access the requested resource")
    return redirect(url_for("index"))


@app.route("/edit_review/<tmdb_id>/<my_reviews_sort>",
           methods=["GET", "POST"])
def edit_review(tmdb_id, my_reviews_sort):
    if check_user_permission() == "valid-user":
        if request.method == "POST":
            review_update = {
                "genre": request.form.get("select-genre"),
                "review": request.form.get("review-text"),
                "rating": request.form.get("inlineRadioOptions"),
                "review_date": datetime.datetime.now()
            }
            mongo.db.reviews.update_one(
                {"tmdb_id": tmdb_id, "created_by": session["user"]},
                {"$set": review_update})
            flash("Your review has been updated")
            return redirect(url_for('my_reviews', user=session['user'],
                                    my_reviews_sort=my_reviews_sort, page=0))
        try:
            media_detail = list(mongo.db.movie_details.find(
                                {"tmdb_id": tmdb_id}))[0]
        except IndexError:
            return redirect(url_for("index"))
        review_fields = list(mongo.db.reviews.find(
            {"tmdb_id": tmdb_id, "created_by": session[
                "user"]}))[0]
        tmdb_poster_url = mongo.db.tmdb_urls.find_one()["tmdb_poster_url"]
        genres = mongo.db.genres.find().sort("genre_name", 1)
        return render_template("edit_review.html", review_fields=review_fields,
                               media_detail=media_detail,
                               tmdb_poster_url=tmdb_poster_url,
                               genres=genres,
                               my_reviews_sort=my_reviews_sort)
    flash("You do not have permission to access the requested resource")
    return redirect(url_for("index"))


@app.route(
    '/review_detail/<tmdb_id>/<media_type>/<review_detail_sort>/<int:page>')
def review_detail(tmdb_id, media_type, review_detail_sort, page):
    if review_detail_sort == "latest":
        reviews = list(mongo.db.reviews.find(
            {"tmdb_id": tmdb_id}).sort("review_date", -1).skip(
                page * 6).limit(6))
    else:
        # Following aggregate based on information in this thread
        # https://stackoverflow.com/questions/9040161/mongo-order-by-length-of-array
        # finds reviews matched by tmdb_id, returns all fields sorted by number
        # of likes
        reviews = list(mongo.db.reviews.aggregate([
            {
                "$match": {"tmdb_id": tmdb_id}
            },
            {
                "$addFields": {
                    "sum_likes": {"$size": {"$ifNull": ["$likes", []]}}}
            },
            {
                "$sort": {"sum_likes": -1}
            },
            {
                "$skip": page * 6
            },
            {
                "$limit": 6
            }
        ]))
    if reviews:
        review_count = mongo.db.reviews.find({"tmdb_id": tmdb_id}).count()
        total_pages = math.ceil(review_count / 6)
        movie_detail = list(mongo.db.movie_details.find(
            {"tmdb_id": tmdb_id}))[0]
        tmdb_poster_url = mongo.db.tmdb_urls.find_one()["tmdb_poster_url"]
        if "user" in session:
            already_reviewed = list(mongo.db.reviews.find({"tmdb_id": tmdb_id,
                                    "created_by": session["user"]}))
        else:
            already_reviewed = False
        overall_rating = 0
        for review in reviews:
            overall_rating += int(review["rating"])
            review["review_date"] = review["review_date"].strftime("%d-%m-%Y")
        session["overall_rating"] = overall_rating
        try:
            overall_rating = round((overall_rating / len(reviews)), 2)
        except ZeroDivisionError:
            flash("Oops we have a zero division error")
        return render_template("review_detail.html", reviews=reviews,
                               movie_detail=movie_detail,
                               tmdb_poster_url=tmdb_poster_url,
                               overall_rating=overall_rating,
                               already_reviewed=already_reviewed,
                               review_detail_sort=review_detail_sort,
                               page=page, review_count=review_count,
                               total_pages=total_pages)
    return redirect(url_for("new_review", tmdb_id=tmdb_id,
                            media_type=media_type))


@app.route("/add_like/<object_id>/<tmdb_id>/<media_type>")
def add_like(object_id, tmdb_id, media_type):
    if check_user_permission() == "valid-user":
        mongo.db.reviews.update_one(
            {"_id": ObjectId(object_id)},
            {"$addToSet": {"likes": session["user"]}})
        return redirect(url_for('review_detail', tmdb_id=tmdb_id,
                                review_detail_sort="popular",
                                media_type=media_type,
                                page=0))
    flash("You do not have permission to access the requested resource")
    return redirect(url_for("index"))


@app.route("/search", methods=["GET", "POST"])
def search_movies():
    if request.method == "POST":
        session["search"] = True
        session["search_query"] = request.form.get("query")
        session["media_type"] = request.form.get("media_type")
        return api_request(page=1)
    session.pop("search_query", None)
    session.pop("media_type", None)
    return render_template("search.html")


@app.route("/search_pagination/<int:page>", methods=["GET", "POST"])
def search_pagination(page):
    if request.method == "POST":
        session["search"] = True
        session["search_query"] = request.form.get("query")
        session["media_type"] = request.form.get("media_type")
        return api_request(page=1)
    if "search_query" in session:
        return api_request(page)
    flash("Something went wrong!")
    return redirect(url_for("search_movies"))


def api_request(page):
    search_url_movie = mongo.db.tmdb_urls.find()[0]['search_url_movie'].format(
        app.api_key, page, session['search_query'])
    search_url_tv = mongo.db.tmdb_urls.find()[0]['search_url_tv'].format(
        app.api_key, page, session['search_query'])
    if session["media_type"] == "tv":
        search_url = search_url_tv
    else:
        search_url = search_url_movie
    try:
        api_search = requests.get(search_url)
    except requests.exceptions.ConnectionError:
        flash("Cannot get results from the database\
                at this time. Please try again later.")
    if api_search.status_code == 200:
        search_results = api_search.json()
        if "results" in search_results:
            return render_template(
                "search.html", search_results=search_results)
        flash("There's been a problem. Please try again later.")
        return None
    flash("Status " + str(api_search.status_code) + " " + api_search.reason + ". \
        Cannot get results from the database at this time. \
            Please try again later.")
    return None


@app.route("/new_review/<tmdb_id>/<media_type>",
           methods=["GET", "POST"])
def new_review(tmdb_id, media_type):
    ''' '''
    if check_user_permission() == "valid-user":
        if request.method == "POST":
            # check if movie details already exist in db and if not, add them
            details_exist = mongo.db.movie_details.find_one(
                {"tmdb_id": tmdb_id})
            if not details_exist:
                # insert new movie details into the db
                session["selected_media"]["overall_rating"] = int(
                    request.form.get("inlineRadioOptions"))
                session["selected_media"]["number_reviews"] = 1
                mongo.db.movie_details.insert_one(dict(
                    session["selected_media"]))
                original_title = session["selected_media"]["original_title"]
            else:
                # update overall rating and number of reviews for sorting
                # purposes
                total_rating = details_exist["overall_rating"] + int(
                    request.form.get("inlineRadioOptions"))
                number_reviews = details_exist["number_reviews"] + 1
                update_rating = total_rating / number_reviews
                mongo.db.movie_details.update_one(
                    {"tmdb_id": tmdb_id},
                    {"$set": {"overall_rating": round(float(
                        update_rating), 2)}})
                mongo.db.movie_details.update_one(
                    {"tmdb_id": tmdb_id},
                    {"$set": {"number_reviews": int(
                        details_exist["number_reviews"] + 1)}})
                mongo.db.movie_details.update_one(
                    {"tmdb_id": tmdb_id},
                    {"$set": {"last_review_date": datetime.datetime.now()}})
                original_title = details_exist["original_title"]
            # Add new review to db
            new_review_object = {
                "tmdb_id": str(tmdb_id),
                "original_title": original_title,
                "genre": request.form.get("select-genre").title(),
                "review": request.form.get("review-text"),
                "rating": request.form.get("inlineRadioOptions"),
                "review_date": datetime.datetime.now(),
                "created_by": session["user"],
                "likes": []
            }
            mongo.db.reviews.insert_one(new_review_object)
            session.pop("selected_media", None)
            session.pop("search_query", None)
            session.pop("media_type", None)
            session.pop("overall_rating", None)
            flash("Review Posted Successfully!")
            return redirect(url_for("browse_reviews", page=0))
    # check if media details are already in db
    if "user" in session:
        already_reviewed = list(mongo.db.reviews.find({"tmdb_id": tmdb_id,
                                "created_by": session["user"]}))
    else:
        already_reviewed = None
    details_exist = list(mongo.db.movie_details.find(
        {"tmdb_id": tmdb_id}))
    if details_exist:
        media_detail = details_exist[0]
    else:
        media_detail = get_choice_detail(tmdb_id, media_type)
        if "status_code" in media_detail:
            if media_detail["status_code"] == 34:
                flash("Sorry. This resource cannot be found.")
                return redirect(url_for("search_movies"))
        else:
            validate_choice(media_detail)
            media_detail = session["selected_media"]
    genres = mongo.db.genres.find().sort("genre_name", 1)
    tmdb_poster_url = mongo.db.tmdb_urls.find_one()["tmdb_poster_url"]
    return render_template("new_review.html", media_detail=media_detail,
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
    if detail_request.status_code == 200:
        if "id" in detail_request.json():
            return detail_request.json()
        flash("There's been a problem. Please try again later.")
        return None

    flash("Status " + str(detail_request.status_code) + " " + detail_request.reason + ". \
        Cannot get results from the database at this time. \
            Please try again later.")
    return None


def validate_api_date_name(media_detail):
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
    validate_api_date_name(media_detail)
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


def add_remove_genre():
    remove_genre = request.form.get("select-genre")
    add_genre = request.form.get("new-genre")
    if remove_genre:
        mongo.db.genres.delete_one(
            {"genre_name": remove_genre})
        flash(f"{remove_genre.title()} Deleted & List Updated")
    if add_genre:
        already_exist = mongo.db.genres.find_one(
            {"genre_name": add_genre.title()})
        if not already_exist:
            mongo.db.genres.insert_one(
                {"genre_name": add_genre.title()})
            flash(f"{add_genre.title()} Added & List Updated")
        else:
            flash("This Entry Already Exists!")
    if not add_genre and not remove_genre:
        flash("Nothing to Update")


def block_users():
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
    unblock_list_users = request.form.getlist("unblock-selected")
    if len(unblock_list_users) != 0:
        for user in unblock_list_users:
            mongo.db.blocked_users.delete_one(
                {"username": user})
        flash("User(s) Unblocked")


@app.route("/admin_controls", methods=["GET", "POST"])
def admin_controls():
    if request.method == "POST":
        if "submit-form-1" in request.form:
            add_remove_genre()
        if "submit-form-3" in request.form:
            block_users()
        if "submit-form-4" in request.form:
            unblock_users()
    if session["user"] == "admin":
        number_users = mongo.db.users.count()
        number_movies = mongo.db.movie_details.count()
        number_reviews = mongo.db.reviews.count()
        most_likes = list(mongo.db.reviews.aggregate([
            {
                "$addFields": {
                    "sum_likes": {"$size": {"$ifNull": ["$likes", []]}}}
            },
            {
                "$sort": {"sum_likes": -1}
            },
            {
                "$limit": 5
            }
        ]))
        # find media_type for the top 5 most liked reviews
        for review in most_likes:
            tmdb_id = review["tmdb_id"]
            movie_detail = mongo.db.movie_details.find_one(
                            {"tmdb_id": tmdb_id})
            review["media_type"] = movie_detail["media_type"]
        genres = mongo.db.genres.find().sort("genre_name", 1)
        user_list = [user["username"] for user in mongo.db.users.find(
            ).sort("username", 1)]
        blocked_users = [user[
            "username"] for user in mongo.db.blocked_users.find(
                ).sort("username", 1)]
        return render_template("admin_controls.html", genres=genres,
                               user_list=user_list,
                               blocked_users=blocked_users,
                               number_users=number_users,
                               number_movies=number_movies,
                               number_reviews=number_reviews,
                               most_likes=most_likes)
    flash("You do not have permission to access the requested resource")
    return redirect(url_for("index"))


@app.route("/contact")
def contact():
    return render_template("contact.html")


def check_user_permission():
    if "user" in session:
        blocked_user = mongo.db.blocked_users.find_one(
            {"username": session["user"].lower()})
        if blocked_user:
            flash("User has been Blocked. Contact the Administrator")
            logout()
            return "user-blocked"
        return "valid-user"
    return False


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username exists in db or is blocked
        username = request.form.get("username")
        blocked_user = mongo.db.blocked_users.find_one(
            {"username": username.lower()})
        if blocked_user:
            flash("User has been Blocked. Contact the Administrator")
            return redirect(url_for("index"))
        existing_user = mongo.db.users.find_one(
            {"username": username.lower()})
        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                session["user"] = username.lower()
                flash(f"Welcome, {username}")
                if username.lower() != "admin":
                    return redirect(url_for("my_reviews", user=session[
                        'user'], my_reviews_sort='latest', page=0))
                return redirect(url_for("admin_controls"))
            # invalid password match
            flash("Incorrect Username and/or Password")
            return redirect(url_for("index"))
        # username doesn't exist
        flash("Incorrect Username and/or Password")
        return redirect(url_for("index"))
    check_user_permission()
    flash("You do not have permission to access the requested resource")
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
            return redirect(url_for("register"))

        password1 = request.form.get("password2")
        password2 = request.form.get("confirm-password2")
        if password1 != password2:
            flash("Passwords do not match!")
            return redirect(url_for("register"))

        new_user = {
            "username": username.lower(),
            "password": generate_password_hash(request.form.get("password2"))
        }
        mongo.db.users.insert_one(new_user)

        # put the new user into 'session' cookie
        session["user"] = username.lower()
        flash("Registration Successful!")
        return redirect(url_for("index"))
    if check_user_permission():
        flash("You do not have permission to access the requested resource")
        return redirect(url_for("index"))
    return render_template("register.html")


@app.route("/change_password", methods=["GET", "POST"])
def change_password():
    if check_user_permission() == "valid-user":
        if request.method == "POST":
            password2 = request.form.get("password2")
            confirm_password2 = request.form.get("confirm-password2")
            if password2 != confirm_password2:
                flash("Passwords do not match!")
                return redirect(url_for("change_password"))

            existing_user = mongo.db.users.find_one(
                {"username": session["user"]})
            if check_password_hash(
                    existing_user["password"], request.form.get("password1")):
                password = generate_password_hash(confirm_password2)
                mongo.db.users.update_one(
                    {"username": session["user"]},
                    {"$set": {"password": password}})
                flash("Password Updated!")
                return redirect(url_for("logout"))
            flash("Passwords do not match!")
            return redirect(url_for("change_password"))
        return render_template("change_password.html")
    flash("You do not have permission to access the requested resource")
    return redirect(url_for("index"))


@app.route("/logout")
def logout():
    if "user" in session:
        # remove user from session cookie
        flash("You have been logged out")
        session.pop("user")
        return redirect(url_for("index"))
    flash("You do not have permission to access the requested resource")
    return redirect(url_for("index"))


@app.errorhandler(404)
def page_not_found(error):
    return render_template("error.html", error=error)


@app.errorhandler(500)
def internal_server_error(error):
    return render_template("error.html", error=error)


@app.errorhandler(CSRFError)
def handle_csrf_error(error):
    return render_template('error.html', error=error.description), 400


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
