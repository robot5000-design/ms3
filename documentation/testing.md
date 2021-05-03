# Testing Report

_* Note all testing was carried out on the deployed version of the site._

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

[1]: ../documentation/images_for_readme/easy-nav.jpg "Easy Navigation"

As the site owner/administrator:

- I want users to be able to register and login.
- I want users to be able to change password.

As a user:

- I want to be able to register and change my password.

_These requirements have been met by providing validated forms for users to register, login and change password._

![Register][2]

[2]: ../documentation/images_for_readme/register.jpg "Register"

![Login][3]

[3]: ../documentation/images_for_readme/login.jpg "Login"

![ChangePassword][4]

[4]: ../documentation/images_for_readme/change-pass.jpg "Change Password"

As the site owner/administrator:

- I want the site to be relatively secure for users.

As a user:

- I want to know that the site is secure and safe to use.

_These requirements have been met by a number of implementations. Mainly, Flask Talisman was used for it's CSP policy, which restricts where the site can load a resource from. It tells the browser to convert all HTTP requests to HTTPS which prevents man-in-the-middle attacks. It also helps to prevent XSS cross-site-scripting attacks. The session cookie is set to secure and times out automatically after 3 hours. Cross-Site Request Forgery (CSRF) attacks are dealt with by CSRFProtect imported from Flask-WTF.csrf. This is used to apply a unique CSRF token to every form on the site. All passwords are hashed using werkzeug.security's generate_password_hash. Certain sensitive information is saved in an env.py environmental variable file which is included in gitignore and so is not pushed to Github. These include, the secret key used to securely sign the session cookie, the TMDB API password and the MongoDB URI.
Below images show results of CSP and security checks by [Google CSP Evaluator](https://csp-evaluator.withgoogle.com/) and [Mozilla Observatory](https://observatory.mozilla.org/) which show that the site evaluated to a high level._

![GoogleCSPEvaluator][5]

[5]: ../documentation/images_for_readme/google-csp.jpg "Google CSP Evaluator"

![MozillaObservatory][6]

[6]: ../documentation/images_for_readme/mozilla-observatory.jpg "Mozilla Observatory"

As the site owner/administrator:

- I want users to be able to search and sort reviews.

As a user:

- I want be able to be able to read, search and sort reviews by all users.

_These requirements have been met by allowing the user to search and sort all reviews on the Browse Reviews page._

![SortAllReviews][7]

[7]: ../documentation/images_for_readme/sort-all-reviews.jpg "Sort All Reviews"

As a user:

- I want to be able to search and sort my reviews.

_These requirements have been met by allowing the user to search and sort their reviews on the My Reviews page._

![MyReviews][8]

[8]: ../documentation/images_for_readme/my-reviews.jpg "My Reviews"

As a user:

- I want to be able to be able to read a specific user reviews.

_These requirements have been met by allowing the user to search and sort another users reviews by clicking on that users name from any review._

![OtherUsers][10]

[10]: ../documentation/images_for_readme/other-users.jpg "Other Users"

As the site owner/administrator:

- I want users to be able to upvote/like other reviews.

As a user:

- I want to be able to 'like' other users reviews to show appreciation.

_These requirements have been met by allowing the user to click on a like/thumbs-up icon which upvotes the review. A user can only upvote a particular review once._

![Upvote][11]

[11]: ../documentation/images_for_readme/upvote.jpg "Upvote"

As the site owner/administrator:

- I want users to be able to make new reviews and edit or delete old reviews.

As a user:

- I want to be able to leave reviews myself and be able to edit, or delete those reviews.

_These requirements have been met by allowing the user to make a new review, edit or delete old reviews._

New Review
![NewReview][12]

[12]: ../documentation/images_for_readme/new-review.jpg "NewReview"

Edit/Delete Review
![EditDeleteReview][13]

[13]: ../documentation/images_for_readme/edit-delete-review.jpg "Edit/Delete Review"

As the site owner/administrator:

- I want users to be able to rate movies and i want the rating to be updated if reviews are adjusted or deleted.

As a user:

- I want to be able to rate movies.

_These requirements have been met by allowing the user to choose a rating value out of 5 using radio inputs._

![EditDeleteReview][14]

[14]: ../documentation/images_for_readme/rating.jpg "Edit/Delete Review"

As the site owner/administrator:

- I want users to be able to see updates or news on the site through social media links.

As a user:

- I want to be able to offer feedback and be aware of updates or new features.

_These requirements have been met by including social links at the bottom of the page as well as a link to a contact form._

Footer:
![Footer][15]

[15]: ../documentation/images_for_readme/footer.jpg "Footer"

Contact Form:
![ContactForm][16]

[16]: ../documentation/images_for_readme/contact-form.jpg "Contact Form"

As the site owner/administrator:

- I want the site to have an admin account with exclusive features, such as, the ability to delete any review on the site or to block a user.
- I want the admin account to have access to some site statistics.

_These requirements have been met by including an exclusive admins controls dashboard with stats and block user functionality._

![AdminControls][17]

[17]: ../documentation/images_for_readme/admin-controls.jpg "Admin Controls"

As the site owner/administrator:

- I want any text inputs by users to be validated.

_These requirements have been met by including form validation on all forms that require it._

![Validation][18]

[18]: ../documentation/images_for_readme/validation.jpg "Form Validation"

As the site owner/administrator:

- I want the site to deal with potential errors without breaking the site or affecting the user negatively.
- I want a site that is not crashing with bugs and if there is an error, that it is managed in a good way for the user.

As a user:

- I want a site that is not commonly crashing with errors, or if there is an error it is managed properly.

_These requirements have been met by employing defensive programming. KeyError's, ZeroDivisionError's, JSONDecodeError's, ConnectionError's, PyMongoError's and RequestException's are all catered for in the code where they could possibly arise. The check_user_permission function checks if users are valid users and is used throughout the program in other functions. If a user is blocked it logs them out. If a user is valid and logged in, it returns "valid-user" otherwise it returns False. This way no matter what route is typed into the address bar, if a user is not valid this will be handled with an appropriate message._

Example of Invalid User:
![InvalidUser][19]

[19]: ../documentation/images_for_readme/invalid-user.jpg "Invalid User"

Example Error:
![ErrorHandling][20]

[20]: ../documentation/images_for_readme/error-handling.jpg "Error Handling"

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

[21]: ../documentation/images_for_readme/w3-warning.jpg "W3C Validator"

Javascript files were passed through jshint.com without any significant issues.

Python code was passed through pylint and there are no outstanding issues.

The Javascript on the site does not function on Internet Explorer 11, but considering its overall low usage and the fact that it is being discontinued in 2021, it was deemed not worth spending time on.

---

## 3. Final Testing Test Cases on Live Website

The site has been tested on both mobile and desktop for responsiveness and functionality. Only manual testing was conducted for this project.

Any issues have been cataloged in the Issues section on Github and closed when a sufficient solution
was reached. There are no known exisiting issues with the final deployed version.

- TC01

    Description:

  - Verify all navbar and footer links on Index page function as expected which will also confirm that the base template links work.

    Procedure:

    1. Navigate to [Index](https://rush-reviews-movies-tv.herokuapp.com/index). Check the navbar logo. It should link to index. __PASS__

    2. Check the navbar menu item links all work as expected. Home, New Review, Browse Reviews, Login. Login should pop up a model. __PASS__

    3. Login and check the user sub-menu in the navbar. My Reviews, Change Password and Logout should all link as expected. __PASS__

    4. After logout press login again but click on 'No Account? Register here'. Should open the Register page. __PASS__

    5. Check the footer links work as expected. Social links should open in a new tab. Contact Us should open the Contact Us page. __PASS__

- TC02

    Description:

  - Verify Register account, Login and Change Password.

    Procedure:

    1. Click on Login in the navbar. Click on 'No Account? Register here'. Try entering a username less than 5 characters and then more than 15. A message should be displayed and it should not be allowed. __PASS__

    2. Try entering symbols for username. Should not be allowed. __PASS__

    3. Repeat steps 1 and 2 for the password. A message should be displayed and it should not be allowed. __PASS__

    4. Register a new username and account. Now try to login. A flash message should welcome the user. __PASS__

    5. Logout and try to login again with the same username but an incorrect password. Should not be allowed. A flash message should appear to say 'Incorrect Username and/or Password'. __PASS__

    6. Try to register the same username. Should not be allowed. A flash message should appear to say 'Username already exists'. __PASS__

    7. Login with the correct password. Click Change Password in the navbar. Check the inputs by repeating steps 1 and 2 for each input. Should not be allowed. __PASS__

    8. Try to change password but with differing new password inputs. A flash message should appear to say 'Passwords do not match!'. __PASS__

    9. Proceed to change password. A flash message should appear to say 'Password Updated'. __PASS__

- TC03

    Description:

  - Verify navbar links on Index page specific to the Admin account, function as expected which will also confirm that the base template links work.

    Procedure:

    1. Navigate to [Index](https://rush-reviews-movies-tv.herokuapp.com/index). Login with admin username and password. Page should redirect to admin control page. __PASS__

    2. Check the navbar menu item my reviews goes to the admin account reviews. __PASS__

    3. Check the navbar submenu admin controls links to the admin controls page. __PASS__

    4. Login as a standard user and verify admin controls menu option is not available. __PASS__

    5. Logout and verify extra menu options for a logged in user are not available. __PASS__

- TC04

    Description:

  - Verify index page content works as expected.

    Procedure:

    1. Navigate to [Index](https://rush-reviews-movies-tv.herokuapp.com/index). Check search input works as expected by performing a search. Results should appear with a url route ending /search_pagination/1 __PASS__

    2. Check that all carousel sizes slide automatically. There are 4 sizes at 3 breakpoints, medium, large and extra-large. One image at screen size smaller than medium, two images at screen size smaller than large, three images at screen size smaller than extra-large and four images at screen size greater than extra-large. __PASS__

    3. Check that carousel images link to the correct movie at each carousel size. __PASS__

    4. Check links in the tables go to the correct users and reviews. __PASS__

- TC05

    Description:

  - Verify New Review Search functionality works correctly.

    Procedure:

    1. Navigate to [New Review](https://rush-reviews-movies-tv.herokuapp.com/search). Verify all inputs are required. Make a search with random numbers. Confirm No Results message. __PASS__

    2. Make a valid search. Check results links works as expected. Should open route ending /new_review/tmdb_id/media, where tmdb_id is an integer and media is tv or movie, if the movie is not already in the database. Otherwise for movies/tv already in the database, should open a route ending /review_detail/tmdb_id/media/popular/0, where tmdb_id is an integer and media is tv or movie. __PASS__

    3. Search with the search term 'marvel', for example. This will result in multiple results. Verify pagination works correctly. Previous should not appear on first page and Next should not appear on last page. __PASS__

- TC06

    Description:

  - Verify New Review page works as intended.

    Procedure:

    1. Logout if logged in. Navigate to [New Review](https://rush-reviews-movies-tv.herokuapp.com/search). Search for and select a movie or tv series that is not already in the database. This can be verified as the route will end in /new_review/tmdb_id/media, where tmdb_id is an integer and media is tv or movie.

    2. The top of page heading should read 'Make New Review'. A message should be displayed 'Please Log-In to submit a Review'. __PASS__

    3. Click 'Please Log-In to submit a Review'. Login Modal should appear. __PASS__

    4. Login with standard user account. Click back until 'Make New Review' appears again. Now the new review form should be displayed. Fill in the required form fields, one by one, pressing the submit button to confirm all inputs are required. __PASS__

    5. Press Submit. Verify loading spinner on button and button disabled. __PASS__

    6. Verify flash message 'Review Posted Successfully!'. Verify Page redirected to Browse Reviews. __PASS__

- TC07

    Description:

  - Verify Overall Ratings and Edit Review page work as intended.

    Procedure:

    1. Login as a standard user and leave a review. Login as a different user and leave another review for the same movie/tv. Navigate to My Reviews. Select Edit/Delete Review for that review. The overall rating should be an average of the two reviews. __PASS__

    2. Modify all inputs. Press Submit. Verify Flash message 'Your review has been updated'. __PASS__

    3. Select Edit/Delete Review for the same review again. Verify the overall rating has updated correctly. __PASS__

    4. Press Delete Review and confirm. Verify Flash message 'Review Successfully Deleted'. Navigate to Browse Reviews and select the same movie again. Confirm Overall Rating has adjusted correctly. Should be the value of the first review in step one. __PASS__

- TC08

    Description:

  - Verify Admin additional features work as intended.

    Procedure:

    1. Confirm that there are reviews in Browse Reviews. Login as Admin. Page should redirect to Admin Controls. __PASS__

    2. Check that the Website Stats on Admin Controls page make sense. __PASS__

    3. Check that the links in Most Popular Reviews redirect to the correct review or the users reviews as expected. __PASS__

    4. Check that a Genre can be added and/or removed. __PASS__

    5. Block a user and logout. Try to login as the blocked user. The flash message 'User has been Blocked. Contact the Administrator', should be displayed. __PASS__

    6. Login as Admin. Select any review and confirm Delete Review deletes only the review selected. If it's the only review of a movie, the movie should automatically be removed from the site. Select another review and confirm Delete Movie deletes the movie from the site. __PASS__

- TC09

    Description:

  - Verify Review Detail works as expected.

    Procedure:

    1. If logged-in, logout. Click on Browse Reviews in the navbar and select any review. This should open a route ending /review_detail/tmdb_id/media/popular/0, where tmdb_id is an integer and media is tv or movie. On the Review Detail page, a message should be displayed 'Please Log-In to submit a Review'. __PASS__

    2. Login. Click on Browse Reviews in the navbar and select any review. Now on the Review Detail page, there should be a Review This button. Click the Review this button and it should open the New Review page. Submit the review. __PASS__

    3. Click on Browse Reviews again. Pick the last review, left in step 2. A message, "You've already reviewed this.", should be displayed. An Edit Review button should be available on that review only. __PASS__

    4. Logout. Click on Browse Reviews again. Pick the last review, left in step 2. The Edit Review button should not be available. __PASS__

    5. Login as a different user. Click on Browse Reviews again. Pick the last review, left in step 2. The Edit Review button should only be available for a review left by the logged-in user. __PASS__

- TC10

    Description:

  - Verify Add Like/Upvote works as expected.

    Procedure:

    1. If logged-in, logout. Select any review. Should not be able to select like (thumbs-up) button. __PASS__

    2. Login. Select one of logged-in users reviews. Should not be able to select like (thumbs-up) button. __PASS__

    3. Select any other users review. Click the like button. The page should reload and that reviews like count should be incremented by 1. It should not now be possible to click the 'like' button for that review again. __PASS__

- TC11

    Description:

  - Verify the Contact Us page works as expected.

    Procedure:

    1. Click on Contact Us in the Footer. Verify all inputs are required. __PASS__

    2. Fill in the form and submit. A message of success 'Status 200' or failure 'Status 400' should be displayed. __PASS__

- TC12

    Description:

  - Verify the Browse Reviews page works as expected.

    Procedure:

    1. Click on Browse Reviews in the navbar. Clicking on any review should link to the Review Detail page. __PASS__

    2. Click Go Back to return to Browse Reviews. Verify that a search input gives the appropriate result. __PASS__

    3. Verify that the Sort dropdown values give the expected sort order. __PASS__

- TC13

    Description:

  - Verify the My Reviews page works as expected.

    Procedure:

    1. Login. Click on My Reviews in the sub-menu of the navbar. Clicking on any review should link to the Edit Review page. __PASS__

    2. Click Go Back to return to My Reviews. Verify that a search input gives the appropriate result. __PASS__

    3. Verify that the Sort dropdown values give the expected sort order. __PASS__

- TC14

    Description:

  - Verify not-logged-in user cannot access certain pages.

    Procedure:

    1. Logout, if logged-in. Type https://rush-reviews-movies-tv.herokuapp.com/change_password into the browser address bar. Page should redirect to index with the flash message 'You do not have permission to access the requested resource'. __PASS__

    2. Type https://rush-reviews-movies-tv.herokuapp.com/admin_controls into the browser address bar. Page should redirect to index with the flash message 'You do not have permission to access the requested resource'. __PASS__

    3. Type https://rush-reviews-movies-tv.herokuapp.com/login into the browser address bar. Page should redirect to index with the flash message 'You do not have permission to access the requested resource'. __PASS__

    4. Type https://rush-reviews-movies-tv.herokuapp.com/logout into the browser address bar. Page should redirect to index with the flash message 'You do not have permission to access the requested resource'. __PASS__

    5. Login. Select a review to Edit/Delete. Then logout. Press the back button on the browser. The page should redirect to index with the flash message 'You do not have permission to access the requested resource'. __PASS__

    6. Login. Select New Review in the navbar and search for a movie that has not already been reviewed. Select the movie and this should open the Make New Review page. Then logout. Press the back button on the browser. The Make New Review page should open again but this time the new review form will not be visible. Instead the message 'Please Log-In to submit a Review'. __PASS__

    7. Login. Select Browse Reviews in the navbar and select any review. Examine the reviews on the review detail page and choose one that has not already been 'liked'. Right click and copy link address for the 'like' thumbs-up icon. Logout. Paste the copied url into the browser address bar and press return. Page should redirect to index with the flash message 'You do not have permission to access the requested resource'. __PASS__

    8. Logout (if logged-in). Select Browse Reviews in the navbar and select any review. The url will be something like https://rush-reviews-movies-tv.herokuapp.com/review_detail/299534/movie/popular/0. The number between review detail and movie(or tv) is the tmdb_id. In this example 299534 is the tmdb_id. Record the tmdb_id in the url. Then type https://rush-reviews-movies-tv.herokuapp.com/delete_review/<tmdb_id> with the tmdb_id added to the end. Page should redirect to index with the flash message 'You do not have permission to access the requested resource'. __PASS__

- TC15

    Description:

  - Verify logged-in user cannot access certain pages.

    Procedure:

    1. Login as standard user. Type https://rush-reviews-movies-tv.herokuapp.com/admin_controls into the browser address bar. Page should redirect to index with the flash message 'You do not have permission to access the requested resource'. __PASS__

    2. Type https://rush-reviews-movies-tv.herokuapp.com/login into the browser address bar. Page should redirect to index with the flash message 'You do not have permission to access the requested resource'. __PASS__

    3. Type https://rush-reviews-movies-tv.herokuapp.com/register into the browser address bar. Page should redirect to index with the flash message 'You do not have permission to access the requested resource'. __PASS__

    4. Select My Reviews from the navbar sub-menu. Click on a movie to edit/delete. Copy the url address. Logout and log-in as a different user. Then either paste the copied url in the address bar or click the browser back button twice. Page should redirect to index with the flash message 'You do not have permission to access the requested resource'. __PASS__

    5. Login. Select Browse Reviews in the navbar and select any review. The url will be something like https://rush-reviews-movies-tv.herokuapp.com/review_detail/299534/movie/popular/0. The number between review detail and movie(or tv) is the tmdb_id. In this example 299534 is the tmdb_id. Record the tmdb_id in the url. Then type https://rush-reviews-movies-tv.herokuapp.com/delete_review/<tmdb_id> with the tmdb_id added to the end. Page should redirect to index with the flash message 'You do not have permission to access the requested resource'. __PASS__

- TC16

    Description:

  - Verify the 404 error page.

    Procedure:

    1. On the home page. Add a random letter to the end of index in the url in the browser address bar. The 404 Not Found error message should be displayed. __PASS__

---

## 4. Testing Site Security

Although difficult to test all aspects of the Talisman CSP policy, the resource restrictions are easy to test by removing the CSP settings. It can be observed through Chrome Development Tools that the resources are now blocked and the site is missing many features including images, styling, Bootstrap, javascript, jquery etc.

The form CSRF protection can be checked by leaving a page with form untouched for over 60 minutes. The CSRF token expires by default after 3600 seconds (60 mins). The CSRF error message is displayed asking the user to go back and refresh the page.

The CSRF token itself can be tested by replacing it with javascript on page load, using $('#csrf_token').val('invalidToken'); and applying the id="csrf_token" attribute to any form to be tested. The 'CSRF token is invalid' error is raised.

To test if the site automatically redirects to https from http for greater security, this can be tested in the browser url address bar, by trying to manually change the address to http. As expected the site automatically loads as https. The security cert information for the site from Chrome Development Tools is shown below.

![devToolsSecurityCert][22]

[22]: ../documentation/images_for_readme/dev-tools-security-cert.jpg "Dev Tools Security Cert"

---

## 5. Other Error/Exception Testing

Other errors or exceptions such as Index, JSON, Connection, Zero Division Exceptions were tested by raising them where expected in the app.py code. The handling of requests and potential errors related to requests to the TMDB API, were tested using http://httpstat.us/. This service can be used to simulate a variety of responses including errors. This url was substituted for the TMDB API url's. Then an integer representing whatever error is to be tested can be added to the end, for example, http://httpstat.us/404 to simulate a 'not found' return. That way, the code and how it handles a variety of responses was tested. After some code adjustement, all potential errors handled as expected.

Any exceptions outside of the scope of those tested, are caught by the Internal Server Error 500 or failing that the catch all, all_other_errors(error) function with decorator @app.errorhandler(Exception). This same function is used to deal with potential Pymongo errors associated with mongodb or request exceptions not caught locally in the code.

A duplicate empty mongodb database was created and this showed that the carousel on the home page was generating index errors. So some conditional statements and appropriate messages for the user were added. Now minimal non-sliding carousels work while reviews are being added until 12 reviews are completed, then carousels function normally. The mobile size carousel will function correctly for any number of reviews.

Chrome Development Tools Lighthouse suggested that some of the buttons had insufficient contrast on the font color, so this text was modified to be more white. It suggested that autocomplete attributes to help password managers were added to all login, register and change password forms, so they were added. It suggested that a hidden username input be added to the change password form to also help password managers.

Examples of the test scores from Chrome Development Tools Lighthouse. In general the scores are very good. The Best Practices section is marked down because of blocked resources due to CSP, but this is what the CSP is there for. Also it mentions that the image resolution is lower than expected. However, these are the largest resolution images supplied through the TMDB API. Some are from quite old movies and they are perfectly adequete for the intended purpose.

![browseReviewsLighthouse][23]

[23]: ../documentation/images_for_readme/browse-reviews-lighthouse.jpg "Browse Reviews Lighthouse"

![reviewDetailLighthouse][24]

[24]: ../documentation/images_for_readme/review-detail-lighthouse.jpg "Review Detail Lighthouse"

---

## 6. Accessibility

The site scores well on Chrome Development Tools Lighthouse for accessibility. Where suggestions of an aria label or descriptor were made, these were put in place. Any suggestions for improving contrast ratio were acted upon.

---

## 7. Debugging

Although there are no known outstanding bugs, the main problematic bugs were reported in the issues section of Github and are copied below.

1. My_reviews not displaying for sorting if no user logged in.

    - Fixed issues #1 & #2 by including missing render_template variables.

2. My_reviews & reviews not rendering after empty search.

    - Fixed issues #1 & #2 by including missing render_template variables.

3. Problem with Flask Talisman blocking some small Bootstrap Icons.

    - Fixed by putting 'data:' in img-src of CSP policy.

4. When click back from a movie detail to search list, search form requires re-submission and therefore page reload.

    - Fixed by redirecting the search through the search pagination function.

5. If user presses submit review multiple times it causes more than one review to be created.

    - Solved by disabling the button with javascript and redirecting away from the page. Works well even with JS disabled.

6. Similar to issue #4 but for browse reviews page. Going back a page requires form resubmission.

    - Solved by same method as issue #4. Redirected through another route search_reviews which negates the issue.

7. Carousel causing index errors when database is empty.

    - Solved by using some conditional statements and now displays a message to the user.

8. After TC15-4 it was possible for a user to see the edit review page of another user.

    - Now it was not possible to actually edit or delete the review, however as a user experience it could be improved so an adjustment was made to the edit_review function.

9. After TC10 Although unlikely it seems that it would be possible to add likes as is.

    - Put another check in the code to see if the current user is in the likes list for that review.

10. After testing discovered reviews without an image did not display properly on the browse reviews or my reviews pages.

    - These images are saved as None in mongodb so solution was to put a conditional jinja in both templates for if the image is saved as None in mongodb.

11. Next page on browse reviews page resets sort order to latest.

    - Solved by adding query and sort order to the route.

12. Next page on my reviews page does not save the search query and the page count is calculated incorrectly.

    - Solved by adding query to the route and modifying the page count statement.

---
