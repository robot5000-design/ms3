import os
import requests
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY")
app.api_key = os.environ.get("API_KEY")
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")

mongo = PyMongo(app)


@app.route('/')
@app.route('/index')
def index():
    session.pop("search_query", None)
    session.pop("media_type", None)
    reviews = list(mongo.db.reviews.find())
    tmdb_poster_url = mongo.db.tmdb_urls.find_one()["tmdb_poster_url"]
    return render_template("index.html", reviews=reviews,
                           tmdb_poster_url=tmdb_poster_url)


@app.route('/review_detail/<tmdb_id>')
def review_detail(tmdb_id):
    reviews = list(mongo.db.reviews.find({"tmdb_id": tmdb_id}))
    flash(reviews)
    return render_template("review_detail.html", tmdb_id=tmdb_id)


@app.route("/search/<int:page_number>", methods=["GET", "POST"])
def search_movies(page_number):
    if request.method == "POST":
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


@app.route("/new_review/<tmdb_id>/<page_number>", methods=["GET", "POST"])
def new_review(tmdb_id, page_number):
    flash(tmdb_id)
    tv_detail_url = mongo.db.tmdb_urls.find()[0]['tv_detail_url'].format(
        tmdb_id, app.api_key)
    movie_detail_url = mongo.db.tmdb_urls.find()[0]['movie_detail_url'].format(
        tmdb_id, app.api_key)
    if "media_type" in session:
        if session["media_type"] == "tv":
            media_detail = requests.get(tv_detail_url).json()
        else:
            media_detail = requests.get(movie_detail_url).json()
    else:
        return redirect(url_for("search_movies", page_number=1))
    if "status_code" in media_detail:
        if media_detail["status_code"] == 34:
            flash("Sorry. This resource cannot be found.")
            return redirect(url_for("search_movies", page_number=page_number))
    else:
        for_review = media_detail
        tmdb_poster_url = mongo.db.tmdb_urls.find_one()["tmdb_poster_url"]
        return render_template(
            "new_review.html", for_review=for_review, page_number=page_number,
            tmdb_poster_url=tmdb_poster_url)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
