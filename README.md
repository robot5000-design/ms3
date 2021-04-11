# Rush Reviews - Movie and TV Series Reviews

## 3rd Milestone Project

## Python & Data-Centric Development

## Code Institute 2021

---

The brief for this project was to build a full-stack website with which users can interact with their own data as well as other users data. Rush Reviews is a movie and tv series review site. The back-end is built using the Flask micro-framework with Jinja templating. A non-relational database MongoDB is used, providing full CRUD operations for users. For the front-end, the Bootstrap 5 framework is used to aid responsiveness and styling. In addition, the site makes use of the TMDB API to allow users to search for movies and ideas of what they would like to review. The design is based on user experience principles. Clean coding and a responsive mobile first method was employed. The purpose of this website is to provide users with:

- an easy and fun to use movie and tv series reviews website.
- a secure user experiance, even though no user personal data is saved.
- a site that is made more relevant and useable because it utilises the TMDB API.
- a smooth and intuitive user interface.
- the ability to browse your own reviews as well as other users.
- the ability to edit or delete reviews.
- the ability to sort and search reviews.
- the ability to upvote other users reviews by giving them a 'like'.
- an exclusive admin dashboard with site stats and the ability to block users and delete any review.

---

### See the image below for an example of the responsiveness of the site.

Click the image to be taken to a live demo of the site:

[![homepage][1]][2]

[1]: ./documentation/images_for_readme/am-i-responsive.jpg
[2]: https://rush-reviews-movies-tv.herokuapp.com "Live Site"

---

### **Contents:**

[1. UX Design](#1-ux-design)

[2. Features and Functionality](#2-features-and-functionality)

[3. Technologies Used](#3-technologies-used)

[4. Testing](#4a-testing-part-1)

[5. Deployment](#5-deployment)

[6. Credits and Notes](#6-credits-and-notes)

---

### **1. UX Design**

#### Strategy

_User Stories:_

There are 2 types of users of the site: the site owner/administrator or all other normal users.

As the site owner/administrator:

- I want the site to be fun and appealing to use and provoke a positive response.
- I want the site layout to be straightforward, simple with smooth navigation between sections.
- I want the site to make use of an API movie database, so that users do not have the laborious task of entering basic information themselves.
- I want users to be able to register and login.
- I want users to be able to change password.
- I want the site to be relatively secure for users.
- I want users to be able to search and sort reviews.
- I want users to be able to make new reviews and edit or delete old reviews.
- I want users to be able to upvote/like other reviews.
- I want users to be able to rate movies and i want the rating to be updated if reviews are adjusted or deleted.
- I want the site to have an admin account with exclusive features, such as, the ability to delete any review on the site or to block a user.
- I want the admin account to have access to some site statistics.
- I want the site to deal with potential errors without breaking the site or affecting the user negatively.
- I want any text inputs by users to be validated.
- I want users to be able to see updates or news on the site through social media links.
- I want a site that is not crashing with bugs and if there is an error, that it is managed in a good way for the user.

As a user:

- I want the site to be fun and appealing to use.
- I want the site to look visually appealing.
- I want the site navigation between sections to be easy.
- I want be able to be able to read, search and sort reviews by all users.
- I want to be able to be able to read a specific user reviews.
- I want to be able to 'like' other users reviews to show appreciation.
- I want to be able to leave reviews myself and be able to edit, or delete those reviews.
- I want to be able to search and sort my reviews.
- I want to be able to register and change my password.
- I want to know that the site is secure and safe to use.
- I want to have access to all the latest movies and tv series, as this will make the site much more interesting to use.
- I want to be able to offer feedback and be aware of updates or new features.
- I want a site that is not commonly crashing with errors, or if there is an error it is managed properly.

#### Scope

From researching other similar review sites, even TMDB's own site, it is clear that they are much bigger and more complex and with many more features than there is time or scope to offer in this project. In future though it would be nice to offer users the ability to share reviews with friends and to follow other users.

Based on the results of the Strategy research the features to be included are:

- Home: Landing page with large obvious CTA and little explanation of site purpose as the purpose should be obvious. A multi image carousel linking to the latest reviews if possible.
- Users can register and login.
- Passwords are validated and hashed.
- Users can change passwords.
- Validate JSON data coming from the TMDB API.
- Handle any API error.
- Handle any JSON parsing error.
- Saves minimal required information on movies being reviewed. That way the site still works even if TMDB API is down.
- Review new movies or series after searching on TMDB API.
- Edit existing entries or delete them.
- View and sort users own entries or the entries of another user.
- Give other users reviews a thumbs-up upvote/like.
- Admin has exclusive access to a dashboard showing stats and info about the site.
- Admin can delete any other users reviews and even a complete movie entry.
- Admin can block and unblock users.
- Attempt to use Flask-Talisman CSP, secure cookies and Flask-WTF CSRF protection.
- Footer: Links to social media and contact us form.

From the strategy table all the above features appear viable. The only feature deemed not viable and outside the scope of this project for the moment, is the ability of users to share content and follow other users.

#### Structure

- A reasonably straightforward structure with 5 basic pages, all accessible from any page from the Navbar at the top of the page. The contact page is accessible from the footer on every page.
- Latest reviewed movies are available through the carousel on the homepage.
- Editing or deletion of reviews is accessed by the user through their own my_reviews page.
- User account features such as my_reviews, change password or log out are accessible through a dropdown sub-menu in the Navbar.
- Custom error page, for 404, 500 and CSRF errors so in the case of a broken internal link or where a CSRF form token has expired, a button is provided for the user to return to safety.

#### Skeleton

Wireframes made in Balsamiq Wireframes were used for basic layout. These can be viewed here:

[Landing Page All Sizes](./documentation/images_for_readme/wireframes/landing_page.png)

[Admin Controls Page All Sizes](./documentation/images_for_readme/wireframes/admin_controls.png)

[Browse Reviews Page All Sizes](./documentation/images_for_readme/wireframes/browse_my_reviews.png)

[New Review Search Page All Sizes](./documentation/images_for_readme/wireframes/new_review_search.png)

[New/Edit Review Page All Sizes](./documentation/images_for_readme/wireframes/new_edit_review.png)

[Review Detail Page All Sizes](./documentation/images_for_readme/wireframes/review_detail.png)

[Register Page All Sizes](./documentation/images_for_readme/wireframes/register.png)

[Change Password Page All Sizes](./documentation/images_for_readme/wireframes/change_password.png)

[Contact Page All Sizes](./documentation/images_for_readme/wireframes/contact_page.png)

#### Surface

[Pixabay](https://pixabay.com/) provided the free background image and the logo is a font-awesome icon enlarged. The main font is a movie style font called Alfa Slab One with the secondary font being Montserrat, both supplied by Google fonts.
The main colors used were #191958 predominant in the background image, #FFA30F for headings, #EEE9E1 for other text, #212529 for the Navbar, #000 for the footer and #316DC6 for some of the buttons.

![ColourChoices][3]

[3]: ./documentation/images_for_readme/palette.png "Colour Choices"

---

### **2. Features and Functionality**

The site was designed with a mobile first approach. Customised Bootstrap was used to help with the responsiveness and layout of the site. In addition targeted media queries were used to assist with this.

Probably the most important feature of the site from a users perspective is the use of the TMDB API as this gives the site a real world relevance for users. From a UX point of view they can spend more time reading and writing reviews on all the available shows.

_Landing Page:_

The landing page features a simple design and layout with a large CTA to search for something to review. There's also easy access to all the latest reviews through the multi image carousel which features a different number of images at different breakpoints. To acheive this, four seperate carousels are used. There is little explanation of how to use the site as the developer didn't feel it would add anything and because the site is self explanatory and straightforward. The navbar gives access to browse reviews or to login. When the user chooses login, a modal appears and if they don't have an account there is a link to the register page.

_Register, Login and Change Password Forms:_

All these forms are validated using a combination of regex patterns on the inputs and Bootstrap javascript for validation messaging.

_Search New Review Form:_

This searches the TMDB API using a python request. As part of defensive programming try/except blocks are used to handle ConnectionError and JSONDecodeError on these requests and returned results. It returns 20 results at a time which are paginated using python and jinja. The results are validated using the validate_choice python function. The results are slightly tricky to validate because all parameters are optional and vary depending on whether it's a movie or tv series.

_Browse Reviews/My Reviews:_

These pages are similar in that they allow the user to sort and search reviews. Browse reviews gives access to read reviews. If a user clicks in to to read details they have the option to leave a review. My reviews on the other hand allows the user to click in to review detail but this time to edit or delete their own review. The my reviews page is also used to display other users reviews when selected for viewing. A user can only review a title once. Both browse reviews and my reviews paginate the results, showing 12 titles at a time (which works great for different screen sizes).

_Review Detail:_

This page allows a user to view details about a movie, such as an image, an overview, an overall rating and reviews left by users. The reviews matching a tmdb_id are picked out of the mongodb reviews collection using a mongodb aggregate which is also used to sum the likes and arrange by most popular. The reviews are paginated, 6 at a time. These reviews can be sorted by popularity or most recent. A logged in user can upvote/like a review. The username is stored in a list array on that review, so the user can only do it once per review. If a user is not logged in, a message is displayed asking them to login if they would like to leave a review. If they are logged in a button will give them the option to leave a review. If they have already reviewed that movie, a message will be displayed advising them that they have already reviewed that title.

_New Review/Edit Review:_

This page is only accessible to logged in users. It contains a form which is used by a user to submit a new review or to edit an existing review. The user can give a rating to a movie. Ratings are adjusted if a review is deleted or the score adjusted.

_Admin Controls:_

This page exclusive to the admin account, allows the admin to see some relevant stats regarding the site and a list of the most popular reviews where they can link directly to the review or user. The admin can also add/remove genres from the genre list, or block/unblock users. It should also be noted the admin account has extra features on the review_detail page. Here there are additional buttons which allows the admin to delete individual reviews or even a complete movie entry and all reviews with it.

_Contact Page:_

Contains a form which can be used by any user to contact the admin. EmailJS is used to provide this service.

_Error Page:_

Used to display error messages such as 404 page not found or 500 internal server error or KeyError exceptions in the code. It is also used to display CSRF errors, such as CSRF token expired. The catch-all exception error handler is used to catch all other exceptions not already caught, such as PyMongoError or RequestException or any others.

_Other features of the backend of the site:_

__Defensive Programming__: As mentioned previously defensive programming was a key consideration. KeyError's, ZeroDivisionError's, IndexError's, JSONDecodeError's, ConnectionError's, PyMongoError's and RequestException's are all catered for in the code where they could possibly arise. The check_user_permission function checks if users are valid users and is used throughout the program in other functions. If a user is blocked it logs them out. If a user is valid and logged in, it returns "valid-user" otherwise it returns False. This way no matter what route is typed into the address bar, if a user is not valid this will be handled with an appropriate message. 

__Security Considerations__: Security was considered for the site in a number of ways. Mainly, Flask Talisman was used for it's CSP policy, which restricts where the site can load a resource from. It tells the browser to convert all HTTP requests to HTTPS which prevents man-in-the-middle attacks. It also helps to prevent XSS cross-site-scripting attacks. The session cookie is set to secure. Cross-Site Request Forgery (CSRF) attacks are dealt with by CSRFProtect imported from Flask-WTF.csrf. This is used to apply a unique CSRF token to every form on the site. All passwords are hashed using werkzeug.security's generate_password_hash. Certain sensitive information is saved in an env.py environmental variable file which is included in gitignore and so is not pushed to Github. These include, the secret key used to securely sign the session cookie, the TMDB API password and the MongoDB URI.

__MongoDB Database Collections Schema__:

![DatabaseSchema][4]

[3]: ./documentation/images_for_readme/database_schema.jpg "Database Schema"






