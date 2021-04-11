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




Rather than having users fill in details on an empty site, it was deemed far more valuable, user friendly and appealing to allow users to sear