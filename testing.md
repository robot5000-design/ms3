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

All HTML and CSS files have been passed through the w3c validation service here https://validator.w3.org/ 
with no significant issues. It advised not to use aria-disabled on disabled buttons. These were removed.

Javascript files were passed through jshint.com without any significant issues. Jshint suggested using
dot notation rather than square brackets, accessing the highscore object, so this has been changed.
Also it suggested that line 650 in main.js !!scienceQuiz.token === false was confusing use of !, so this 
was changed to Boolean(scienceQuiz.token) === false.

The site does not function on Internet Explorer 11, but considering its overall low usage and the fact that
it is being discontinued in 2021, it was deemed not worth spending time on.

---

## 3. Final Testing Test Cases on Live Website:
- TC01

    Description: 

    - Verify all links on Index page function as expected.

    Procedure: 





The site has been tested on both mobile and desktop for responsiveness. Only manual testing was
conducted for this project.

Any issues have been cataloged in the Issues section on Github and closed when a sufficient solution
was reached. Prior to final testing of the live site, functional testing was carried out using judiciously 
placed console logs before they were removed. These are saved in a separate file [here](./documentation/manual-test-ref.md)
and are included only for reference. There are no known exisiting issues with the final deployed version.



All HTML and CSS files have been passed through the w3c validation service https://validator.w3.org/ with no significant issues.