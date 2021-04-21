'''Rush Reviews Main Application Module.

Contains all the routes and runs an instance of the app.
'''
import os
import datetime
import math
import pymongo
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
from helper_functions import (
    block_users, unblock_users, validate_choice,
    add_remove_genre, insert_new_movie, update_overall_rating,
    get_choice_detail, api_request)
from constants import CSP, TMDB_URLS
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

# Applies Talisman CSP protection to the app
talisman = Talisman(app,
                    force_https=True,
                    content_security_policy_nonce_in=['script-src'],
                    content_security_policy=CSP)

# Applies CSRF protection for all forms
csrf = CSRFProtect(app)

mongo = PyMongo(app)


@app.route('/', methods=["GET", "POST"])
@app.route('/index', methods=["GET", "POST"])
def index():
    """ Retrieves the last 12 movies or tv series reviewed and renders
    the index template.

    Also facilitates the TMDB API search input.

    Returns:
        The index template with last 12 reviewed movies if they exist or
        not.
        If POST request returns the results of the TMDB API request.
    """
    if request.method == "POST":
        session["search"] = True
        session["search_query"] = request.form.get("query")
        session["media_type"] = request.form.get("media_type")
        return api_request(page=1)
    media_detail = list(mongo.db.media_details.find().sort(
        "last_review_date", -1).limit(12))
    if media_detail:
        tmdb_poster_url = TMDB_URLS["tmdb_poster_url"]
        return render_template("index.html", media_detail=media_detail,
                               tmdb_poster_url=tmdb_poster_url)
    return render_template("index.html")


@app.route("/browse_reviews/<int:page>", methods=[
           "GET", "POST"])
def browse_reviews(page):
    """ Used to facilitate a redirect to the search_reviews function
    to prevent form resubmission requests in browser on page back.

    Args:
        page (int): A page number to facilate pagination of the reviews
        template.

    Returns:
        A redirect to the search_reviews function and if a POST request,
        returns a redirect to the search_reviews function using the search
        form inputs.
    """
    if request.method == "POST":
        query = request.form.get("search-box")
        browse_reviews_sort = request.form.get("browse_reviews_sort")
        if not query:
            query = "all"
        return redirect(url_for("search_reviews", query=query,
                                browse_reviews_sort=browse_reviews_sort,
                                page=page))
    query = "all"
    browse_reviews_sort = "latest"
    return redirect(url_for("search_reviews", query=query,
                            browse_reviews_sort="browse_reviews_sort",
                            page=page))


@app.route("/search_reviews/<query>/<browse_reviews_sort>/<int:page>",
           methods=["GET", "POST"])
def search_reviews(query, browse_reviews_sort, page):
    """ Handles paginated display of all reviews.

    Displays 12 reviews at a time sorted from the database by latest,
    most popular or rating. A POST request with a search query can filter
    the results further.

    Args:
        query (str): Search input if POST request.
        browse_reviews_sort (str): Describes sort order.
        page (int): A page number to facilate pagination of the reviews
        template.

    Returns:
        A render template of all reviews, 12 at a time paginated, or if POST
        request reults can be filtered or reordered.
        If KeyError is raised return render template of error.html.

    Raises:
        KeyError: If the tmdb_poster_url is modified incorrectly in database
        TMDB_URLS collection.
    """
    if request.method == "POST":
        query = request.form.get("search-box")
        browse_reviews_sort = request.form.get("browse_reviews_sort")
        if query:
            search_term = {"$text": {"$search": query}}
        else:
            search_term = None
            query = ""
    else:
        if query == "all":
            search_term = None
            query = ""
        else:
            search_term = {"$text": {"$search": query}}
    review_count = mongo.db.media_details.find(search_term).count()
    total_pages = math.ceil(review_count / 12)
    if browse_reviews_sort == "rating":
        media_detail = list(mongo.db.media_details.find(search_term).sort(
            "overall_rating", -1).skip(page * 12).limit(12))
    elif browse_reviews_sort == "popularity":
        media_detail = list(mongo.db.media_details.find(search_term).sort(
            "number_reviews", -1).skip(page * 12).limit(12))
    else:
        media_detail = list(mongo.db.media_details.find(search_term).sort(
            "last_review_date", -1).skip(page * 12).limit(12))
    if media_detail:
        try:
            tmdb_poster_url = TMDB_URLS["tmdb_poster_url"]
        except KeyError as error:
            error = f"Key Error: {error}"
            return render_template("error.html", error=error)
        return render_template("reviews.html", media_detail=media_detail,
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
    """ Handles paginated display of a users reviews.

    Displays 12 reviews at a time sorted from the database by latest,
    alphabetically or oldest. A POST request with a search query can filter
    the results further.

    Args:
        user (str): Username of results to be displayed.
        my_reviews_sort (str): Describes sort order.
        page (int): A page number to facilate pagination of the my_reviews
        template.

    Returns:
        A render template of a users reviews, 12 at a time paginated, or if
        POST request reults can be filtered or reordered.
        If KeyError is raised return render template of error.html.

    Raises:
        KeyError: If the tmdb_poster_url is modified incorrectly in database
        TMDB_URLS collection.
    """
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
        media_detail = []
        iteration = 0
        while iteration < len(movie_id_list):
            movie_details = mongo.db.media_details.find(
                {"tmdb_id": movie_id_list[iteration]})
            media_detail.extend(movie_details)
            iteration += 1
        if media_detail:
            try:
                tmdb_poster_url = TMDB_URLS["tmdb_poster_url"]
            except KeyError as error:
                error = f"Key Error: {error}"
                return render_template("error.html", error=error)
        return render_template("my_reviews.html", media_detail=media_detail,
                               tmdb_poster_url=tmdb_poster_url,
                               page=page, my_reviews_sort=my_reviews_sort,
                               review_count=review_count,
                               total_pages=total_pages,
                               user=user, query=query)
    return render_template("my_reviews.html", user=user,
                           my_reviews_sort=my_reviews_sort, page=page)


@app.route("/delete_review/<tmdb_id>/<user>")
def delete_review(tmdb_id, user):
    """ Handles deleting a review from the database reviews collection.

    Checks if a valid user. A valid user must be logged in. Looks up
    the review and deletes it. Also deletes the movie details if there
    are no other reviews. Otherwise adjusts the overall rating and number
    of reviews. If due to a miscalculation in the database over time, the
    rating goes above 5, it is set equal to 5.

    Args:
        tmdb_id (str): This is the id that TMDB API use to identify a certain
        movie or tv series.
        user (str): Username of user logged into session cookie.

    Returns:
        If user is admin a redirect to browse_reviews.
        Otherwise any other user, a redirect to my_reviews.
        If invalid user a redirect to index.

    Raises:
        ZeroDivisionError: if updated_number_reviews = 0
    """
    if check_user_permission() == "valid-user":
        if user == session["user"] or session["user"] == "admin":
            review_to_delete = mongo.db.reviews.find_one(
                {"tmdb_id": tmdb_id, "created_by": user.lower()})
            mongo.db.reviews.delete_one(review_to_delete)
            flash("Review Successfully Deleted")
            # check if there are other reviews, otherwise delete movie
            # details in the db
            other_reviews = mongo.db.reviews.find_one(
                {"tmdb_id": tmdb_id})
            if not other_reviews:
                mongo.db.media_details.delete_one(
                    {"tmdb_id": tmdb_id})
            else:
                # adjust the overall rating to take account of deleted review
                details_exist = mongo.db.media_details.find_one(
                    {"tmdb_id": tmdb_id})
                current_rating = details_exist["overall_rating"]
                current_number_reviews = details_exist["number_reviews"]
                deleted_rating = float(review_to_delete["rating"])
                updated_number_reviews = current_number_reviews - 1
                try:
                    updated_overall_rating = (
                        (current_rating * current_number_reviews) -
                        deleted_rating) / updated_number_reviews
                except ZeroDivisionError:
                    flash("Oops, division by zero error")
                    updated_overall_rating = current_rating
                if updated_overall_rating > 5:
                    updated_overall_rating = 5
                update_items = {
                    "overall_rating": round(updated_overall_rating, 2),
                    "number_reviews": updated_number_reviews
                }
                mongo.db.media_details.update_one(
                    {"tmdb_id": tmdb_id},
                    {"$set": update_items})
            if session["user"] == "admin":
                return redirect(url_for('browse_reviews', page=0))
            return redirect(url_for('my_reviews', user=user,
                                    my_reviews_sort='latest', page=0))
    flash("You do not have permission to access the requested resource")
    return redirect(url_for("index"))


@app.route("/delete_review/<tmdb_id>")
def delete_all(tmdb_id):
    """ Allows admin user to delete all entries in mongodb for a certain
    movie or tv series.

    Args:
        tmdb_id (str): This is the id that TMDB API use to identify a certain
        movie or tv series.

    Returns:
        If user is admin, it returns a redirect to browse_reviews after
        deletion.
        If no user in session or user is not admin, returns a redirect to
        index.
    """
    if check_user_permission() == "valid-user":
        if session["user"] == "admin":
            mongo.db.reviews.delete_many(
                {"tmdb_id": tmdb_id})
            mongo.db.media_details.delete_one(
                {"tmdb_id": tmdb_id})
            flash("Movie & Reviews Successfully Deleted")
            return redirect(url_for('browse_reviews', page=0))
    flash("You do not have permission to access the requested resource")
    return redirect(url_for("index"))


@app.route("/edit_review/<tmdb_id>/<my_reviews_sort>",
           methods=["GET", "POST"])
def edit_review(tmdb_id, my_reviews_sort):
    """ Handles editing of user reviews.

    First, checks if a valid user is in session cookie with
    check_user_permission. If not it redirects to index. Otherwise it obtains
    movie and review details from mongodb and renders the edit_review template.
    If POST request, it prepares a review update object populated with the form
    inputs. It updates the overall rating and then inserts the review and
    updates the media_details. It then redirects the user to my_reviews.

    Args:
        tmdb_id (str): This is the id that TMDB API use to identify a certain
        movie or tv series.
        my_reviews_sort (str): Describes sort order.

    Returns:
        If there are valid results from mongodb it returns render of template
        for edit_reviews.html.
        Upon successful completion of a review edit, it returns a redirect to
        my_reviews.
        If IndexError or invalid user, it returns a redirect to index.

    Raises:
        ZeroDivisionError: If current_number_reviews = 0
        IndexError: If the movie or tv series cannot be found in mongodb.
    """
    if check_user_permission() == "valid-user":
        if request.method == "POST":
            review_update = {
                "genre": request.form.get("select-genre"),
                "review": request.form.get("review-text"),
                "rating": request.form.get("inlineRadioOptions"),
                "review_date": datetime.datetime.now()
            }
            # adjust the overall rating to take account of edited review
            media_detail = mongo.db.media_details.find_one(
                {"tmdb_id": tmdb_id})
            existing_review = mongo.db.reviews.find_one(
                {"tmdb_id": tmdb_id, "created_by": session["user"]})
            current_overall_rating = media_detail["overall_rating"]
            current_number_reviews = media_detail["number_reviews"]
            existing_review_rating = float(existing_review["rating"])
            adjusted_review_rating = float(request.form.get(
                "inlineRadioOptions"))
            try:
                updated_overall_rating = round(float(((
                    current_overall_rating * current_number_reviews)
                    - existing_review_rating + adjusted_review_rating)
                    / current_number_reviews), 2)
            except ZeroDivisionError:
                flash("Oops, division by zero error")
                updated_overall_rating = current_overall_rating
            if updated_overall_rating > 5:
                updated_overall_rating = 5
            mongo.db.media_details.update_one(
                {"tmdb_id": tmdb_id},
                {"$set": {"overall_rating": updated_overall_rating}})
            mongo.db.reviews.update_one(
                {"tmdb_id": tmdb_id, "created_by": session["user"]},
                {"$set": review_update})
            flash("Your review has been updated")
            return redirect(url_for('my_reviews', user=session['user'],
                                    my_reviews_sort=my_reviews_sort, page=0))
        try:
            media_detail = mongo.db.media_details.find_one(
                                {"tmdb_id": tmdb_id})
            review_fields = mongo.db.reviews.find_one(
                {"tmdb_id": tmdb_id, "created_by": session[
                    "user"]})
        except IndexError:
            flash("That resource does not exist")
            return redirect(url_for("index"))
        tmdb_poster_url = TMDB_URLS["tmdb_poster_url"]
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
    """ Handles getting detailed information about a movie or tv series and
    pagination of reviews.

    First, it finds reviews for the selected movie or series if they exist,
    sorted either by latest or by most likes, 6 at a time for pagination.
    If there are reviews, it then counts how many for pagination. It then
    finds the movie details and checks if the user in session has already
    reviewed the movie. It puts the overall_rating in the session and formats
    the review date for each review. It then renders the review_detail
    template.

    Args:
        tmdb_id (str): This is the id that TMDB API use to identify a certain
        movie or tv series.
        media_type (str): Used to identify whether the search is for a movie
        or tv series and to use the approriate API url.
        review_detail_sort (str): Describes sort order.
        page (int): A page number to facilate pagination of the my_reviews
        template.

    Returns:
        If there are no valid results from mongodb it returns a redirect to
        new_review.
        if there are reviews but no movie details in mongodb, this results in
        an index error and returns a redirect to index.
        Otherwise it returns a render of the review_details template.

    Raises:
        IndexError: If the movie or tv series cannot be found in mongodb.
    """
    if review_detail_sort == "latest":
        reviews = list(mongo.db.reviews.find(
            {"tmdb_id": tmdb_id}).sort("review_date", -1).skip(
                page * 6).limit(6))
    else:
        # The following aggregate is based on information in this thread
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
        try:
            media_detail = mongo.db.media_details.find_one(
                {"tmdb_id": tmdb_id})
        except IndexError:
            flash("That resource does not exist")
            return redirect(url_for("index"))
        tmdb_poster_url = TMDB_URLS["tmdb_poster_url"]
        if "user" in session:
            already_reviewed = mongo.db.reviews.find_one(
                {"tmdb_id": tmdb_id, "created_by": session["user"]})
        else:
            already_reviewed = False
        overall_rating = media_detail["overall_rating"]
        session["overall_rating"] = overall_rating
        for review in reviews:
            review["review_date"] = review["review_date"].strftime("%d-%m-%Y")
        return render_template("review_detail.html", reviews=reviews,
                               media_detail=media_detail,
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
    """ Handles the add like functionality.

    First, checks if a valid user is in session cookie with
    check_user_permission, otherwise redirects them to index. It then adds the
    user to the likes list of the review in question. It then redirects the
    user back review_detail.

    Args:
        object_id (hexadecimal): This is the mongodb id representing each
        document in a collection.
        tmdb_id (str): This is the id that TMDB API use to identify a certain
        movie or tv series.
        media_type (str): Used to identify whether the search is for a movie
        or tv series and to use the approriate API url.

    Returns:
        Upon updating the collection with adding a like, it returns a redirect
        to review_detail.
        If not a valid user, flashes an appropriate message and returns a
        redirect to index.
    """
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
    """ Handles search form for new reviews.

    This function serves as a redirect to the search_pagination
    function, to avoid form resubmission on page back in the browser.
    On page load, it deletes relevant session entries. It handles
    the search form entries and redirects to search_pagination for page 1
    of results.

    Returns:
        A render of the search.html template.
        If POST request returns a redirect to search_pagination for page 1
        of results.
    """
    if request.method == "POST":
        session["search"] = True
        session["search_query"] = request.form.get("query")
        session["media_type"] = request.form.get("media_type")
        return redirect(url_for("search_pagination", page=1))
    session.pop("search_query", None)
    session.pop("media_type", None)
    return render_template("search.html")


@app.route("/search_pagination/<int:page>", methods=["GET", "POST"])
def search_pagination(page):
    """ Handles search_pagination of TMDB API for new reviews.

    Args:
        page (int): The API returns 20 results at a time. Page number is used
        to select results page required.

    Returns:
        A redirect to search_movies.
        If a search query already in session it returns a call of the
        api_request function.
        If POST request returns a call of the api_request function.
    """
    if request.method == "POST":
        session["search"] = True
        session["search_query"] = request.form.get("query")
        session["media_type"] = request.form.get("media_type")
        return api_request(page=1)
    if "search_query" in session:
        return api_request(page)
    return redirect(url_for("search_movies"))


@app.route("/new_review/<tmdb_id>/<media_type>",
           methods=["GET", "POST"])
def new_review(tmdb_id, media_type):
    """ Handles inputting a new review into the database.

    First, checks if a valid user is in session cookie with
    check_user_permission. Then checks if the user has already reviewed the
    movie. Then checks if the movie details already exist in the database
    media_details collection. If they do not, get_choice_details is called.
    This invokes a request to the TMDB API for the details. Then confirms the
    results are valid, before rendering the new_review template.
    If POST request for a new review, it checks if the movie details exist. If
    not, it inserts the details in the database media_details collection. It
    then updates the movie overall rating and prepares and inserts the
    new_review object. Relevant items are then removed from the session cookie.

    Args:
        tmdb_id (str): This is the id that TMDB API use to identify a certain
        movie or tv series.
        media_type (str): Used to identify whether the search is for a movie
        or tv series and to use the approriate API url.

    Returns:
        Upon selecting a movie or tv series to review it returns a render
        of the new_review template.
        If a succesful POST request, returns a redirect to browse_reviews.
        If incomplete data is returned from the API request, it returns
        a redirect to search_movies.
    """
    if check_user_permission() == "valid-user":
        if request.method == "POST":
            # check if movie details already exist in db and if not, add them
            details_exist = mongo.db.media_details.find_one(
                {"tmdb_id": tmdb_id})
            if not details_exist:
                insert_new_movie()
                original_title = session["selected_media"]["original_title"]
            else:
                # update overall rating and number of reviews for sorting
                # purposes
                update_items = update_overall_rating(details_exist)
                mongo.db.media_details.update_one(
                    {"tmdb_id": tmdb_id},
                    {"$set": update_items})
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
        already_reviewed = mongo.db.reviews.find_one(
            {"tmdb_id": tmdb_id, "created_by": session["user"]})
    else:
        already_reviewed = None
    details_exist = mongo.db.media_details.find_one(
        {"tmdb_id": tmdb_id})
    if details_exist:
        media_detail = details_exist
    else:
        media_detail = get_choice_detail(tmdb_id, media_type)
        # check the results returned are of valid type
        if isinstance(media_detail, dict) and "status_code" in media_detail:
            if media_detail["status_code"] == 34:
                flash("Sorry. This resource cannot be found.")
                return redirect(url_for("search_movies"))
        if isinstance(media_detail, dict) and "id" in media_detail:
            validate_choice(media_detail)
            media_detail = session["selected_media"]
        else:
            return redirect(url_for("search_movies"))
    genres = mongo.db.genres.find().sort("genre_name", 1)
    tmdb_poster_url = TMDB_URLS["tmdb_poster_url"]
    return render_template("new_review.html", media_detail=media_detail,
                           genres=genres,
                           tmdb_poster_url=tmdb_poster_url,
                           already_reviewed=already_reviewed)


@app.route("/admin_controls", methods=["GET", "POST"])
def admin_controls():
    """ Exclusive controls for the admin user account.

    Checks user permission and that user is admin and then renders the
    admin_controls template. Extracts stats from various collections in
    the database.
    Genre list, user list and blocked user list from their corresponding
    collections, for the forms on admin_controls template. most_likes is
    a list of 5 most popular reviews.
    Otherwise flashes an appropriate message and redirects the
    user to index route.

    Returns:
        If user is in session and is admin, returns render of admin_controls.
        If user is not admin returns redirect to index route.
    """
    if request.method == "POST":
        if "submit-form-1" in request.form:
            add_remove_genre()
        if "submit-form-3" in request.form:
            block_users()
        if "submit-form-4" in request.form:
            unblock_users()
    if check_user_permission() and session["user"] == "admin":
        number_users = mongo.db.users.count()
        number_movies = mongo.db.media_details.count()
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
            media_detail = mongo.db.media_details.find_one(
                {"tmdb_id": tmdb_id})
            review["media_type"] = media_detail["media_type"]
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
    """ Returns render of contact template
    """
    return render_template("contact.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """ Facilitates a user to login to the site.

    Checks user permission. If user already in session it redirects to index.
    Otherwise the POST request through the login modal is validated and
    handled. The username is checked to see if it is on the blocked users list.
    If blocked the user is not logged in. Otherwise the username and passord
    are checked against those saved in the database and if matching the
    username is saved in the session cookie.

    Returns:
        If blocked user, or user already in session returns a redirect to index
        route.
        If valid user and POST request and username and password match,
        returns redirect to my_reviews route.
        If valid user and POST request and username and password match, if
        username is admin returns redirect to admin_controls route.
        If valid user and POST request and username or password do not match,
        returns redirect to index route.
    """
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
                flash(f"Welcome, {username.capitalize()}")
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
    """ Facilitates a user to register on the site.

    Checks user permission. If user not in session it renders the register
    template. Otherwise the user is redirected to index route. A user can
    choose a username and password. Username is checked if it already exists
    in the database. The password is input twice and checked for matching.
    When valid inputs are submitted the username and hashed password are
    inserted to the database.

    Returns:
        If invalid user, returns a redirect to index route.
        If valid user, returns render of register template.
        If valid user and POST request and username already exists or
        passwords do not match, returns redirect to register route, otherwise
        returns redirect to index route.
    """
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
    """ Facilitates a user to change their password.

    Checks user permission. If valid it renders the change_password template.
    Otherwise the user is redirected to index route. If a valid user requests
    to change password, it checks if new passwords match, generates a new hash
    based on the new password and updates it to the database.

    Returns:
        If invalid user, returns a redirect to index route.
        If valid user, returns render of change_password template.
        If valid user and POST request and passwords do not match, redirects
        to change_password route, otherwise redirects to logout.
    """
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
    """ Logs out a user by removing them from the session, flashes an
    appropriate message, then redirects to index route.
    If no user in session, flashes an appropriate message and redirects
    to index route.

    Returns:
        In any case returns a redirect to index route.
    """
    if "user" in session:
        # remove user from session cookie
        flash("You have been logged out")
        session.pop("user")
        return redirect(url_for("index"))
    flash("You do not have permission to access the requested resource")
    return redirect(url_for("index"))


@app.errorhandler(404)
def page_not_found(error):
    """ Handles a 404 page not found error
    """
    return render_template("error.html", error=error)


@app.errorhandler(500)
def internal_server_error(error):
    """ Handles a 500 internal server error
    """
    return render_template("error.html", error=error)


@app.errorhandler(Exception)
def all_other_errors(error):
    """ Catch all. Handles all other errors.
    """
    if isinstance(error, pymongo.errors.PyMongoError):
        error = "System Error: Internal Database Error."
    elif isinstance(error, requests.exceptions.RequestException):
        error = "System Error: Problem connecting with TMDB API."
    else:
        error = f"System Error: {error}"
    return render_template("error.html", error=error)


@app.errorhandler(CSRFError)
def handle_csrf_error(error):
    """ Handles a CSRF token expired error
    """
    error = f"For security: {error.description} Go back and \
        Refresh the page and try again."
    return render_template('error.html', error=error), 400


def check_user_permission():
    """ Checks if a user is in the session cookie and if they are blocked.

    Returns:
        If user not in session returns False.
        If user in session and blocked returns 'user-blocked'.
        if user in session and not blocked returns 'valid-user'.
    """
    if "user" in session:
        blocked_user = mongo.db.blocked_users.find_one(
            {"username": session["user"].lower()})
        if blocked_user:
            flash("User has been Blocked. Contact the Administrator")
            logout()
            return "user-blocked"
        return "valid-user"
    return False


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
