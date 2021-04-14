# Testing Report

## 1. Compare User Test Cases

The first part of testing was to confirm that all user stories requirements have been met. There is large crossover between both sets of user stories.

As the site owner/administrator:

- I want the site to be fun and appealing to use and provoke a positive response.
- I want the site layout to be straightforward, simple with smooth navigation between sections.
- I want the site to make use of an API movie database, so that users do not have the laborious task of entering basic information themselves.

As a user:

- I want the site to be fun and appealing to use.
- I want the site to look visually appealing.
- I want the site navigation between sections to be easy.
- I want to have access to all the latest movies and tv series, as this will make the site much more interesting to use.

_These requirements have been met by a bold interface with eye-catching font and colors. The permanent navbar provides for easy, smooth navigation between sections and the users own account. The large CTA on the home page allows the user to search the TMDB API for something to review._

![EasyNavigation][1]

[1]: ./documentation/images_for_readme/easy-nav.jpg "Easy Navigation"

As the site owner/administrator:

- I want users to be able to register and login.
- I want users to be able to change password.

As a user:

- I want to be able to register and change my password.

_These requirements have been met by providing validated forms for users to register, login and change password._

![Register][2]

[2]: ./documentation/images_for_readme/register.jpg "Register"

![Login][3]

[3]: ./documentation/images_for_readme/login.jpg "Login"

![ChangePassword][4]

[4]: ./documentation/images_for_readme/change-pass.jpg "Change Password"

As the site owner/administrator:

- I want the site to be relatively secure for users.

As a user:

- I want to know that the site is secure and safe to use.

_These requirements have been met by a number of implementations. Mainly, Flask Talisman was used for it's CSP policy, which restricts where the site can load a resource from. It tells the browser to convert all HTTP requests to HTTPS which prevents man-in-the-middle attacks. It also helps to prevent XSS cross-site-scripting attacks. The session cookie is set to secure. Cross-Site Request Forgery (CSRF) attacks are dealt with by CSRFProtect imported from Flask-WTF.csrf. This is used to apply a unique CSRF token to every form on the site. All passwords are hashed using werkzeug.security's generate_password_hash. Certain sensitive information is saved in an env.py environmental variable file which is included in gitignore and so is not pushed to Github. These include, the secret key used to securely sign the session cookie, the TMDB API password and the MongoDB URI.
Below images show results of CSP and security checks by [Google CSP Evaluator](https://csp-evaluator.withgoogle.com/) and [Mozilla Observatory](https://observatory.mozilla.org/) which show that the site evaluated to a high level._

![GoogleCSPEvaluator][5]

[5]: ./documentation/images_for_readme/google-csp.jpg "Google CSP Evaluator"

![MozillaObservatory][6]

[6]: ./documentation/images_for_readme/mozilla-observatory.jpg "Mozilla Observatory"

As the site owner/administrator:

- I want users to be able to search and sort reviews.

As a user:

- I want be able to be able to read, search and sort reviews by all users.

_These requirements have been met by allowing the user to search and sort all reviews on the Browse Reviews page._

![SortAllReviews][7]

[7]: ./documentation/images_for_readme/sort-all-reviews.jpg "Sort All Reviews"

As a user:

- I want to be able to search and sort my reviews.

_These requirements have been met by allowing the user to search and sort their reviews on the My Reviews page._

![MyReviews][8]

[8]: ./documentation/images_for_readme/my-reviews.jpg "My Reviews"

As a user:

- I want to be able to be able to read a specific user reviews.

_These requirements have been met by allowing the user to search and sort another users reviews by clicking on that users name from any review._

![OtherUsers][10]

[10]: ./documentation/images_for_readme/other-users.jpg "Other Users"

As the site owner/administrator:

- I want users to be able to upvote/like other reviews.

As a user:

- I want to be able to 'like' other users reviews to show appreciation.

_These requirements have been met by allowing the user to click on a like/thumbs-up icon which upvotes the review. A user can only upvote a particular review once._

![Upvote][11]

[11]: ./documentation/images_for_readme/upvote.jpg "Upvote"

As the site owner/administrator:

- I want users to be able to make new reviews and edit or delete old reviews.

As a user:

- I want to be able to leave reviews myself and be able to edit, or delete those reviews.

_These requirements have been met by allowing the user to make a new review, edit or delete old reviews._

New Review
![NewReview][12]

[12]: ./documentation/images_for_readme/new-review.jpg "NewReview"

Edit/Delete Review
![EditDeleteReview][13]

[13]: ./documentation/images_for_readme/edit-delete-review.jpg "Edit/Delete Review"

As the site owner/administrator:

- I want users to be able to rate movies and i want the rating to be updated if reviews are adjusted or deleted.

As a user:

- I want to be able to rate movies.

_These requirements have been met by allowing the user to choose a rating value out of 5 using radio inputs._

![EditDeleteReview][14]

[14]: ./documentation/images_for_readme/rating.jpg "Edit/Delete Review"

As the site owner/administrator:

- I want users to be able to see updates or news on the site through social media links.

As a user:

- I want to be able to offer feedback and be aware of updates or new features.

_These requirements have been met by including social links at the bottom of the page as well as a link to a contact form._

Footer:
![Footer][15]

[15]: ./documentation/images_for_readme/footer.jpg "Footer"

Contact Form:
![ContactForm][16]

[16]: ./documentation/images_for_readme/contact-form.jpg "Contact Form"

As the site owner/administrator:

- I want the site to have an admin account with exclusive features, such as, the ability to delete any review on the site or to block a user.
- I want the admin account to have access to some site statistics.

_These requirements have been met by including an exclusive admins controls dashboard with stats and block user functionality._

![AdminControls][17]

[17]: ./documentation/images_for_readme/admin-controls.jpg "Admin Controls"

As the site owner/administrator:

- I want any text inputs by users to be validated.

_These requirements have been met by including form validation on all forms that require it._

![Validation][18]

[18]: ./documentation/images_for_readme/validation.jpg "Form Validation"

As the site owner/administrator:

- I want the site to deal with potential errors without breaking the site or affecting the user negatively.
- I want a site that is not crashing with bugs and if there is an error, that it is managed in a good way for the user.

As a user:

- I want a site that is not commonly crashing with errors, or if there is an error it is managed properly.

_These requirements have been met by employing defensive programming. KeyError's, ZeroDivisionError's, IndexError's, JSONDecodeError's, ConnectionError's, PyMongoError's and RequestException's are all catered for in the code where they could possibly arise. The check_user_permission function checks if users are valid users and is used throughout the program in other functions. If a user is blocked it logs them out. If a user is valid and logged in, it returns "valid-user" otherwise it returns False. This way no matter what route is typed into the address bar, if a user is not valid this will be handled with an appropriate message._

Example of Invalid User:
![InvalidUser][19]

[19]: ./documentation/images_for_readme/invalid-user.jpg "Invalid User"

Example Error:
![ErrorHandling][20]

[20]: ./documentation/images_for_readme/error-handling.jpg "Error Handling"

---

## 2. Page Responsiveness

### Testing responsiveness of each html page

Using Chrome and Chrome Dev Tools.

Breakpoints | index | admin controls | change password | contact | edit review | new review | register | login | review detail | search | browse reviews | my reviews | error
--- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---
W280px | y | y | y | y | y | y | y | y | y | y | y | y | y | y
W400px | y | y | y | y | y | y | y | y | y | y | y | y | y | y
W576px | y | y | y | y | y | y | y | y | y | y | y | y | y | y
W768px | y | y | y | y | y | y | y | y | y | y | y | y | y | y
W992px | y | y | y | y | y | y | y | y | y | y | y | y | y | y
W1200px | y | y | y | y | y | y | y | y | y | y | y | y | y | y

- In addition, each page is checked for responsiveness using Chrome Dev Tools infinitely adjustable sliding re-sizer tool. From 280px (Samsung Galaxy Fold) up to full width 1536px on a 4k laptop. Although not optimised for 280px, it is perfectly useable.
- All tests passed.

### __Summary:__

- No problems found.

---

## 3. List of devices tested

- Google Pixel 5
- Samsung Galaxy S7
- Samsung A21s
- Samsung Galaxy S10
- Huawei P30 Pro
- iPhone 11 Safari through Browserstack (limited test)
- Asus k501u 4k laptop
- Chrome Dev Tools Device Emulator:
  - Samsung Galaxy Fold
  - Samsung S5
  - Google Pixel 2
  - iPhone 5
  - iPhone X
  - iPad
  - iPad Pro

The site has been tested on the following browsers on Windows 10:

- Internet Explorer 11
- Firefox 87.0
- Google Chrome 89.0.4389.114
- Opera 75.0.3969.149
- Microsoft Edge 89.0.774.68
- Safari 10.1 on Mac using www.browserstack.com (limited test)

and tested on a Google Pixel 5:

- Chrome 89.0.4389.105

All HTML and CSS files have been passed through the w3c validation service here https://validator.w3.org/ with the only issue raised in relation to CSP as shown below. Considering the positive reports on the Google CSP Evaluator and Mozilla Observatory CSP evaluator, this w3 warning is being ignored for now.

![w3cValidator][21]

[21]: ./documentation/images_for_readme/w3-warning.jpg "W3C Validator"

Javascript files were passed through jshint.com without any significant issues.

Python code was passed through pylint and there are no outstanding issues.

The Javascript on the site does not function on Internet Explorer 11, but considering its overall low usage and the fact that it is being discontinued in 2021, it was deemed not worth spending time on.

---

## 3. Final Testing Test Cases on Live Website:

The site has been tested on both mobile and desktop for responsiveness and functionality. Only manual testing was conducted for this project.

Any issues have been cataloged in the Issues section on Github and closed when a sufficient solution
was reached. There are no known exisiting issues with the final deployed version.

- TC01

    Description:

  - Verify all navbar and footer links on Index page function as expected which will also confirm that the base template links work.

    Procedure:

    1. Navigate to [Index](https://rush-reviews-movies-tv.herokuapp.com/index). Check the navbar logo. It should link to index. __PASS__

    2. Check the navbar menu item links all work as expected. Home, New Review, Browse Reviews, Login. Login should pop up a model. __PASS__

    3. Login and check the user sub-menu in the navbar. My Reviews, Change Password and Logout should all work as expected. __PASS__

    4. After logout press login again but click on 'No Account? Register here'. Should open the Register page. __PASS__

    5. Check the footer links work as expected. Social links should open in a new tab. Contact Us should open the Contact Us page. __PASS__

- TC02

    Description:

  - Verify navbar links on Index page specific to the Admin account, function as expected which will also confirm that the base template links work.

    Procedure:

    1. Navigate to [Index](https://rush-reviews-movies-tv.herokuapp.com/index). Login with admin username and password. Page should redirect to admin control page. __PASS__

    2. Check the navbar menu item my reviews goes to the admin account reviews. __PASS__

    3. Check the navbar submenu admin controls links to the admin controls page. __PASS__

- TC03

    Description:

  - Verify index page content works as expected.

    Procedure:

    1. Navigate to [Index](https://rush-reviews-movies-tv.herokuapp.com/index). Check search input works as expected by performing a search. Results should appear with a url route ending /search_pagination/1 __PASS__

    2. Check that all carousel sizes slide automatically. There are 4 sizes at 3 breakpoints, medium, large and extra-large. One image at screen size smaller than medium, two images at screen size smaller than large, three images at screen size smaller than extra-large and four images at screen size greater than extra-large. __PASS__

    3. Check that carousel images link to the correct movie at each carousel size. __PASS__

- TC04

    Description:

  - Verify New Review Search functionality works correctly.

    Procedure:

    1. Navigate to [New Review](https://rush-reviews-movies-tv.herokuapp.com/search). Verify all inputs are required. Make a search with random numbers. Confirm No Results message. __PASS__

    2. Make a valid search. Check results links works as expected. Should open route ending /new_review/tmdb_id/media, where tmdb_id is an integer and media is tv or movie, if the movie is not already in the database. Otherwise for movies/tv already in the database, should open a route ending /review_detail/tmdb_id/media/popular/0, where tmdb_id is an integer and media is tv or movie. __PASS__

    3. Search with the search term 'marvel', for example. Verify pagination works correctly. Previous should not appear on first page and Next should not appear on last page. __PASS__

- TC05

    Description:

  - Verify New Review page works as intended.

    Procedure:

    1. Logout if logged in. Navigate to [New Review](https://rush-reviews-movies-tv.herokuapp.com/search). Search for and select a movie or tv series that is not already in the database. This can be verified as the route will end in /new_review/tmdb_id/media, where tmdb_id is an integer and media is tv or movie.

    2. The top of page heading should read 'Make New Review'. A message should be displayed 'Please Log-In to submit a Review'. __PASS__

    3. Click 'Please Log-In to submit a Review'. Login Modal should appear. __PASS__

    4. Login with standard user account. Click back until 'Make New Review' appears again. Now the new review form should be displayed. Fill in the required form fields, one by one, pressing the submit button to confirm all inputs are required. __PASS__

    5. Press Submit. Verify loading spinner on button and button disabled. __PASS__

    6. Verify flash message 'Review Posted Successfully!'. Verify Page redirected to Browse Reviews. __PASS__

- TC06

    Description:

  - Verify Overall Ratings and Edit Review page work as intended.

    Procedure:

    1. Login as a standard user and leave a review. Login as a different user and leave another review for the same movie/tv. Navigate to My Reviews. Select Edit/Delete Review for that review. The overall rating should be an average of the two reviews. __PASS__

    2. Modify all inputs. Press Submit. Verify Flash message 'Your review has been updated'. __PASS__

    3. Select Edit/Delete Review for the same review again. Verify the overall rating has updated correctly. __PASS__

    4. Press Delete Review and confirm. Verify Flash message 'Review Successfully Deleted'. Navigate to Browse Reviews and select the same movie again. Confirm Overall Rating has adjusted correctly. Should be the value of the first review in step one. __PASS__

- TC07

    Description:

  - Verify Admin additional features work as intended.

    Procedure:

    1. Confirm that there are reviews in Browse Reviews. Login as Admin. Page should redirect to Admin Controls. __PASS__

    2. 