import os
import requests
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY")
app.api_key = os.environ.get("API_KEY")


@app.route('/')
def hello_world():
    session.clear()
    return render_template("base.html")


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
    search_url_movie = f"https://api.themoviedb.org/3/search/movie?api_key={app.api_key}&language=en-US&page={page_number}&\
            include_adult=false&query={session['search_query']}"
    search_url_tv = f"https://api.themoviedb.org/3/search/tv?api_key={app.api_key}&language=en-US&page={page_number}&\
        include_adult=false&query={session['search_query']}"
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


@app.route("/review/<tmdb_id>/<page_number>", methods=["GET", "POST"])
def review(tmdb_id, page_number):
    flash(tmdb_id)
    tv_detail_url = f"https://api.themoviedb.org/3/tv/{tmdb_id}?api_key={app.api_key}&language=en-US"
    movie_detail_url = f"https://api.themoviedb.org/3/movie/{tmdb_id}?api_key={app.api_key}&language=en-US"
    if session["media_type"] == "tv":
        media_detail = requests.get(tv_detail_url).json()
    else:
        media_detail = requests.get(movie_detail_url).json()
    if "status_code" in media_detail:
        if media_detail["status_code"] == 34:
            flash("Sorry. This resource cannot be found.")
            return redirect(url_for("search_movies", page_number=page_number))
    else:
        for_review = media_detail
        return render_template(
            "review.html", for_review=for_review, page_number=page_number)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
