'''Helper functions for the main application.

api_request: searches and renders results from the TMDB API
get_choice_detail: gets media details from the TMDB API
insert_new_movie: inserts a new movie or series to mongodb collection
update_overall_rating: adjusts the overall rating after a review is edited
validate_choice: validates data returned from the TMDB API
add_remove_genre: used by admin account to add or remove a genre
block_users: used by admin account to block a user account
unblock_users: used by admin account to unblock a user account
'''
import os
import datetime
import json
import requests
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from constants import TMDB_URLS
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

mongo = PyMongo(app)


def api_request(page):
    """ Gets data from the TMDB API based on a search term and whether it is
    a tv series or a movie.

    Gets the TMDB API urls from the TMDB_URLS database collection. Different
    TMDB API urls are used depending on whether tv series or a movie.

    Args:
        page (int): The API returns 20 results at a time. Page number is used
        to select results page required.

    Returns:
        If there are valid results it returns render of template for
        search.html.
        If there is a request connection error, incomplate data returned, a
        json conversion error, or anything but a request status 200, it returns
        a redirect to search_movies.

    Raises:
        ConnectionError: If there is a problem connecting the the TMDB API.
        JSONDecodeError: If the return from the request cannot be converted
        to json.
    """
    search_url_movie = TMDB_URLS["search_url"].format(
        media="movie", api_key=app.api_key, page=page,
        query=session['search_query'])
    search_url_tv = TMDB_URLS["search_url"].format(
        media="tv", api_key=app.api_key, page=page,
        query=session['search_query'])
    if session["media_type"] == "tv":
        search_url = search_url_tv
    else:
        search_url = search_url_movie
    try:
        api_search = requests.get(search_url)
    except requests.exceptions.ConnectionError:
        flash("Cannot connect to the TMDB database\
            at this time. Please try again later.")
        return redirect(url_for("search_movies"))
    if api_search.status_code == 200:
        try:
            search_results = api_search.json()
        except json.decoder.JSONDecodeError:
            flash("There's been a problem with the results. Please try again \
            later.")
            return redirect(url_for("search_movies"))
        if "results" in search_results:
            return render_template(
                "search.html", search_results=search_results)
        flash("There's been a problem with the results. Please try again \
            later.")
        return redirect(url_for("search_movies"))
    flash("Status " + str(api_search.status_code) + " " + api_search.reason + ". \
        Cannot get results from the database at this time. \
            Please try again later.")
    return redirect(url_for("search_movies"))


def get_choice_detail(tmdb_id, media_type):
    """ Gets detail of a certain selected movie or tv series from the TMDB
    API using the tmdb_id and media_type.

    Gets the TMDB API urls from the TMDB_URLS database collection. Media type
    is saved to the session cookie. Different TMDB API urls are used depending
    on whether tv series or a movie.

    Args:
        tmdb_id (str): This is the id that TMDB API use to identify a certain
        movie or tv series.
        media_type (str): Used to identify whether the search is for a movie
        or tv series and to use the approriate API url.

    Returns:
        If there are no errors returns media_detail, valid detailed results of
        the movie or tv series chosen for the request.
        An error flash message if there's a problem with the request, e.g. a
        connection problem.
        Redirects to search_movies route with a flash error message, if the
        request data cannot be converted to json.
        Returns "request-error" if can connect to the TMDB database but does
        not return a status 200.

    Raises:
        ConnectionError: If there is a problem connecting the the TMDB API.
        JSONDecodeError: If the return from the request cannot be converted
        to json.
    """
    tv_detail_url = TMDB_URLS["detail_url"].format(
        media="tv", tmdb_id=tmdb_id, api_key=app.api_key)
    movie_detail_url = TMDB_URLS["detail_url"].format(
        media="movie", tmdb_id=tmdb_id, api_key=app.api_key)
    session["media_type"] = media_type
    if media_type == "tv":
        detail_url = tv_detail_url
    else:
        detail_url = movie_detail_url
    try:
        detail_request = requests.get(detail_url)
    except requests.exceptions.ConnectionError:
        return flash("Cannot connect to the TMDB database\
                     at this time. Please try again later.")
    if detail_request.status_code == 200:
        if isinstance(detail_request, requests.models.Response):
            try:
                media_detail = detail_request.json()
            except json.decoder.JSONDecodeError:
                flash("There's been a problem with the results. Please try again \
                    later.")
                return redirect(url_for("search_movies"))
            else:
                return media_detail
    flash("Status " + str(detail_request.status_code) + " " + detail_request.reason + ". \
        Cannot get results from the TMDB database at this time. \
        Please try again later.")
    return "request-error"


def insert_new_movie():
    """ Add and initialise rating and number of reviews to the selected_media
    session object and insert object of new movie details into the database
    media_details collection.
    """
    session["selected_media"]["overall_rating"] = int(
        request.form.get("inlineRadioOptions"))
    session["selected_media"]["number_reviews"] = 1
    mongo.db.media_details.insert_one(dict(
        session["selected_media"]))


def update_overall_rating(details_exist):
    """ Update overall rating, number of reviews and date of review. If
    due to a miscalculation in the database over time, the rating goes
    above 5, it is set equal to 5.

    Returns:
        update_items (dict): Contains updated values for overall rating,
        number of reviews and date of last review.

    Args:
        details_exist (obj): Cursor object returned from mongodb of details
        of a specific movie or tv series.

    Raises:
        ZeroDivisionError: if number_reviews = 0
    """
    total_rating = ((details_exist["overall_rating"]
                    * details_exist["number_reviews"])
                    + float(request.form.get("inlineRadioOptions")))
    number_reviews = details_exist["number_reviews"] + 1
    try:
        updated_overall_rating = total_rating / number_reviews
    except ZeroDivisionError:
        flash("Oops we have a zero division error")
        updated_overall_rating = total_rating
    if updated_overall_rating > 5:
        updated_overall_rating = 5
    update_items = {
        "overall_rating": round(float(updated_overall_rating), 2),
        "number_reviews": int(details_exist["number_reviews"] + 1),
        "last_review_date": datetime.datetime.now()
    }
    return update_items


def validate_api_date_name(media_detail):
    """ Validates and extracts movie release date data returned from the
    TMDB API and saves it to the session cookie as a dictionary.

    Args:
        media_detail: json object returned from TMDB API request.
    """
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
    """ Validates and extracts data returned from the TMDB API and saves
    it to the session cookie as a dictionary.

    Args:
        media_detail: json object returned from TMDB API request.
    """
    session["selected_media"] = {}
    if "id" in media_detail:
        session["selected_media"]["tmdb_id"] = str(media_detail["id"])
    if "original_title" in media_detail:
        session["selected_media"][
            "original_title"] = media_detail["original_title"]
    elif "original_name" in media_detail:
        session["selected_media"][
            "original_title"] = media_detail["original_name"]
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
    session["selected_media"]["media_type"] = session["media_type"]
    validate_api_date_name(media_detail)


def add_remove_genre():
    """ Both adds and removes genres from the genres collection.

    Gets values from the select-genre and new-genre inputs which are used
    to add a genre if it doesn't exist or remove genres from the genres
    database collection.
    """
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
