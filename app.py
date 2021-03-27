import os
import requests
import datetime
import math
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from flask_talisman import Talisman
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


@app.route("/browse_reviews/<sort_by>/<int:page>", methods=[
    "GET", "POST"], defaults={'sort_by': 'latest', 'page': 0})
def browse_reviews(sort_by, page):
    if request.method == "POST":
        query = request.form.get("search-box")
        sort_by = request.form.get("sort_by")
        if query:
            search_term = {"$text": {"$search": query}}
        else:
            search_term = None
    else:
        search_term = None
        query = ""
    review_count = mongo.db.movie_details.find(search_term).count()
    total_pages = math.ceil(review_count / 12)
    if sort_by == "rating":
        movie_details = list(mongo.db.movie_details.find(search_term).sort(
            "overall_rating", -1).skip(page * 12).limit(12))
    elif sort_by == "popularity":
        movie_details = list(mongo.db.movie_details.find(search_term).sort(
            "number_reviews", -1).skip(page * 12).limit(12))
    else:
        movie_details = list(mongo.db.movie_details.find(search_term).sort(
            "last_review_date", -1).skip(page * 12).limit(12))
    if movie_details:
        tmdb_poster_url = mongo.db.tmdb_urls.find_one()["tmdb_poster_url"]
        return render_template("reviews.html", movie_details=movie_details,
                               tmdb_poster_url=tmdb_poster_url,
                               sort_by=sort_by, page=page,
                               review_count=review_count,
                               total_pages=total_pages,
                               query=query)
    return render_template("reviews.html")


@app.route("/my_reviews/<user>/<sort_by>/<int:page>", methods=[
    "GET", "POST"])
def my_reviews(user, sort_by, page):
    if request.method == "POST":
        query = request.form.get("search-box")
        sort_by = request.form.get("sort_by")
        if query:
            search_term = {"$text": {"$search": query}, "created_by": user}
        else:
            search_term = {"created_by": user}
    else:
        search_term = {"created_by": user}
        query = ""
    if sort_by == "alphabetically":
        my_reviews = list(mongo.db.reviews.find(search_term).sort(
            "original_title", 1).skip(page * 6).limit(6))
    elif sort_by == "oldest":
        my_reviews = list(mongo.db.reviews.find(search_term).sort(
            "review_date", 1).skip(page * 6).limit(6))
    else:
        my_reviews = list(mongo.db.reviews.find(search_term).sort(
            "review_date", -1).skip(page * 6).limit(6))
    if my_reviews:
        movie_id_list = []
        for review in my_reviews:
            movie_id_list.append(review["tmdb_id"])
        review_count = mongo.db.reviews.find({"created_by": user}).count()
        total_pages = math.ceil(review_count / 6)
        # pick out the movies details that we need
        movie_details = []
        index = 0
        while index < len(movie_id_list):
            movie_detail = list(mongo.db.movie_details.find(
                {"tmdb_id": movie_id_list[index]}))
            movie_details.extend(movie_detail)
            index += 1
        if movie_details:
            tmdb_poster_url = mongo.db.tmdb_urls.find_one()["tmdb_poster_url"]
        return render_template("my_reviews.html", movie_details=movie_details,
                               tmdb_poster_url=tmdb_poster_url,
                               page=page, sort_by=sort_by,
                               review_count=review_count,
                               total_pages=total_pages,
                               user=user, query=query)
    return render_template("my_reviews.html", user=user)


@app.route("/delete_review/<tmdb_id>/<user>")
def delete_review(tmdb_id, user):
    if user == session["user"] or session["user"] == "admin":
        mongo.db.reviews.delete_one(
            {"tmdb_id": tmdb_id, "created_by": user.lower()})
        flash("Review Successfully Deleted")
        other_reviews = mongo.db.reviews.find_one(
            {"tmdb_id": tmdb_id})
        if not other_reviews:
            mongo.db.movie_details.delete_one(
                {"tmdb_id": tmdb_id})
        if session["user"] == "admin":
            return redirect(url_for('browse_reviews'))
        else:
            return redirect(url_for('my_reviews'))


@app.route("/delete_review/<tmdb_id>")
def delete_all(tmdb_id):
    if session["user"] == "admin":
        mongo.db.reviews.delete_many(
            {"tmdb_id": tmdb_id})
        mongo.db.movie_details.delete_one(
            {"tmdb_id": tmdb_id})
        flash("Movie & Reviews Successfully Deleted")
    return redirect(url_for('browse_reviews'))


@app.route("/edit_review/<tmdb_id>",
           methods=["GET", "POST"])
def edit_review(tmdb_id):
    if request.method == "POST":
        mongo.db.reviews.update_one(
            {"tmdb_id": tmdb_id, "created_by": session["user"]},
            {"$set": {"genre": request.form.get("select-genre")}})
        mongo.db.reviews.update_one(
            {"tmdb_id": tmdb_id, "created_by": session["user"]},
            {"$set": {"review": request.form.get("review-text")}})
        mongo.db.reviews.update_one(
            {"tmdb_id": tmdb_id, "created_by": session["user"]},
            {"$set": {"rating": request.form.get("inlineRadioOptions")}})
        mongo.db.reviews.update_one(
            {"tmdb_id": tmdb_id, "created_by": session["user"]},
            {"$set": {"review_date": datetime.datetime.now()}})
        flash("Your review has been updated")
        return redirect(url_for('my_reviews', user=session['user'],
                                sort_by='latest', page=0))
    media_detail = list(mongo.db.movie_details.find({"tmdb_id": tmdb_id}))[0]
    review_fields = list(mongo.db.reviews.find(
        {"tmdb_id": tmdb_id, "created_by": session[
            "user"]}))[0]
    tmdb_poster_url = mongo.db.tmdb_urls.find_one()["tmdb_poster_url"]
    genres = mongo.db.genres.find().sort("genre_name", 1)
    return render_template("edit_review.html", review_fields=review_fields,
                           media_detail=media_detail,
                           tmdb_poster_url=tmdb_poster_url,
                           genres=genres)


@app.route('/review_detail/<tmdb_id>/<sort_by>')
def review_detail(tmdb_id, sort_by):
    if sort_by == "latest":
        reviews = list(mongo.db.reviews.find(
            {"tmdb_id": tmdb_id}).sort("review_date", -1))
    else:
        # Following aggregate based on information in this thread
        # https://stackoverflow.com/questions/9040161/mongo-order-by-length-of-array
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
            }
        ]))
    if reviews:
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
                               sort_by=sort_by)
    else:
        return redirect(url_for("index.html"))


@app.route("/add_like/<id>/<tmdb_id>")
def add_like(id, tmdb_id):
    mongo.db.reviews.update_one(
        {"_id": ObjectId(id)},
        {"$addToSet": {"likes": session["user"]}})
    return redirect(url_for('review_detail', tmdb_id=tmdb_id,
                            sort_by="popular"))


@app.route("/search/<int:page>", methods=["GET", "POST"])
def search_movies(page):
    if request.method == "POST":
        session["search"] = True
        session["search_query"] = request.form.get("query")
        session["media_type"] = request.form.get("media_type")
        return api_request(page)
    session.pop("search_query", None)
    session.pop("media_type", None)
    return render_template("search.html")


@app.route("/search_pagination/<int:page>")
def search_pagination(page):
    flash("Page " + str(page))
    if "search_query" in session:
        return api_request(page)
    else:
        return redirect(url_for("search_movies", page=1))


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


@app.route("/new_review/<tmdb_id>/<media_type>/<page>",
           methods=["GET", "POST"])
def new_review(tmdb_id, media_type, page):
    if request.method == "POST":
        # check if movie details already exist in db and if not, add them
        details_exist = mongo.db.movie_details.find_one(
            {"tmdb_id": tmdb_id})
        if not details_exist:
            # insert new movie details into the db
            session["selected_media"]["overall_rating"] = int(request.form.get(
                "inlineRadioOptions"))
            session["selected_media"]["number_reviews"] = 1
            mongo.db.movie_details.insert_one(dict(session["selected_media"]))
            original_title = session["selected_media"]["original_title"]
        else:
            # update overall rating and number of reviews for sorting purposes
            total_rating = details_exist["overall_rating"] + int(
                request.form.get("inlineRadioOptions"))
            number_reviews = details_exist["number_reviews"] + 1
            update_rating = total_rating / number_reviews
            mongo.db.movie_details.update_one(
                {"tmdb_id": tmdb_id},
                {"$set": {"overall_rating": round(float(update_rating), 2)}})
            mongo.db.movie_details.update_one(
                {"tmdb_id": tmdb_id},
                {"$set": {"number_reviews": int(
                    details_exist["number_reviews"] + 1)}})
            mongo.db.movie_details.update_one(
                {"tmdb_id": tmdb_id},
                {"$set": {"last_review_date": datetime.datetime.now()}})
            original_title = details_exist["original_title"]
        # Add new review to db
        new_review = {
            "tmdb_id": str(tmdb_id),
            "original_title": original_title,
            "genre": request.form.get("select-genre").title(),
            "review": request.form.get("review-text"),
            "rating": request.form.get("inlineRadioOptions"),
            "review_date": datetime.datetime.now(),
            "created_by": session["user"],
            "likes": []
        }
        mongo.db.reviews.insert_one(new_review)
        session.pop("selected_media", None)
        session.pop("search_query", None)
        session.pop("media_type", None)
        session.pop("overall_rating", None)
        flash("Review Posted Successfully!")
        return redirect(url_for("browse_reviews"))
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
                return redirect(url_for("search_movies", page=page))
        else:
            validate_choice(media_detail)
            media_detail = session["selected_media"]
    genres = mongo.db.genres.find().sort("genre_name", 1)
    tmdb_poster_url = mongo.db.tmdb_urls.find_one()["tmdb_poster_url"]
    return render_template(
        "new_review.html", media_detail=media_detail,
        page=page,
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


@app.route("/admin_controls", methods=["GET", "POST"])
def admin_controls():
    if request.method == "POST":
        if "submit-form-1" in request.form:
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
                    flash("Entry Already in List")
            if not add_genre and not remove_genre:
                flash("Nothing to Update")
        if "submit-form-2" in request.form:
            delete_list_users = request.form.getlist("select-user")
            if len(delete_list_users) == 0:
                for user in delete_list_users:
                    mongo.db.users.delete_one(
                        {"username": user})
                flash("Users Deleted")
            else:
                flash("Nothing to Update")
    if "user" in session:
        if session["user"] == "admin":
            genres = mongo.db.genres.find().sort("genre_name", 1)
            user_list = [user["username"] for user in mongo.db.users.find(
                ).sort("username", 1)]
            return render_template("admin_controls.html", genres=genres,
                                   user_list=user_list)
        else:
            return redirect(url_for("index"))
    else:
        return redirect(url_for("index"))


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
                return redirect(url_for("my_reviews", user=session[
                    'user'], sort_by='latest', page=0))
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


@app.route("/change_password", methods=["GET", "POST"])
def change_password():
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
        else:
            flash("Passwords do not match!")
            return redirect(url_for("change_password"))
    if "user" in session:
        return render_template("change_password.html")
    else:
        return redirect(url_for("index"))


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
