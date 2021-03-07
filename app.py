import os
import requests
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
app = Flask(__name__)


#req = requests.get("")


@app.route('/')
def hello_world():
    return render_template("base.html")


@app.route("/search", methods=["GET", "POST"])
def search_movies():
    if request.method == "POST":
        search_query = request.form.get("query")
        search_results = requests.get(
            f"https://api.themoviedb.org/3/search/movie?api_key=8d3e922f5f3ff83d99d9b723cc6fe7dd&language=en-US\
                    &page=1&include_adult=false&query={search_query}"
            ).json()
        session["search_results"] = search_results["results"]
        return render_template("search.html", results=session.search_results)
    return render_template("search.html")


@app.route("/review/<tmdb_id>", methods=["GET", "POST"])
def review(tmdb_id):
    return render_template("review.html", results=session.search_results)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
