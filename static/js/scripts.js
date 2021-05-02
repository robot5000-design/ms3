// Regular Functions  ######################################################################

/**
 * Sends the feedback form values to the emailjs service template
 * @param { object } contactForm - feedback form values
 */
 function sendMail(contactForm) {
    emailjs.send("service_ceipqpk", "template_7pribcf", {
        "from_name": contactForm.name.value,
        "from_email": contactForm.emailaddress.value,
        "feed_back": contactForm.feedback.value
    })
        .then(
            function (response) {
                handleMailResponse(response, `Your message has been successfully delivered.`);
            },
            function (error) {
                handleMailResponse(error, `Sorry. There's been a problem and your mail has not been sent. Please try again later.`);
            }
        );
    return false; // To block from loading a new page
}

/**
 * emailjs initialisation 
 */
(function () {
    emailjs.init("user_oV8YdlKemUPQdjcjpZQbo");
})();

/**
 * Sends the feedback form values to the emailjs service template
 * @param { object } responseObject - emailjs.send response object
 * @param { string } message - message to display to user on success or failure
 */
function handleMailResponse(responseObject, message) {
    $(".contact-error").html(
        `<div>
            Status: ${responseObject.status}
        </div>
        <div>
            ${message}
        </div>`
    );
    $(".contact-form")[0].reset();
    removeLoadingSpinner(".submit-contact", "Contact Admin");
}

/**
 * Form validation taken directly from bootstrap documentation
 * Disables form submissions if there are invalid fields
 */
(function () {
    'use strict';
    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    var forms = document.querySelectorAll('.needs-validation');
    // Loop over them and prevent submission
    Array.prototype.slice.call(forms)
        .forEach(function (form) {
            form.addEventListener('submit', function (event) {
                if (!form.checkValidity()) {
                    event.preventDefault();
                    event.stopPropagation();
                } else {
                    addLoadingSpinner(".change-pass-btn");
                    addLoadingSpinner(".login-btn");
                    addLoadingSpinner(".register");
                }
                form.classList.add('was-validated');
            }, false);
        });
})();

/**
 * Adds a loading spinner and disables the button referenced as the argument
 * @param { string } toThisButton - button to which function is applied
 */
function addLoadingSpinner(toThisButton) {
    $(toThisButton).html("<span class='spinner-border spinner-border-sm' role='status' aria-hidden='true'></span> Loading...");
    $(toThisButton).prop("disabled", true);
}

/**
 * Replaces a loading spinner and enables the button referenced as the toThisButton argument
 * and replaces the html text of the button with the buttonText argument
 * @param { string } toThisButton - button to which function is applied
 * @param { string } buttonText - button html text to apply
 */
function removeLoadingSpinner(toThisButton, buttonText) {
    $(toThisButton).html(buttonText);
    $(toThisButton).prop("disabled", false);
}

/**
 * When the go-back button is clicked the browser returns to the
 * previous page in history
 */
function goBack() {
    window.history.back();
}

// Click and Submit Events ###################################################################################

// makes the delete process a two step process. Press the call-delete
// button  and the confirm-delete goes from invisible to visible
$(".delete-genre").click(function () {
    $(this).addClass("invisible");
    $(this).siblings(".confirm-genre").removeClass("invisible");
});

// On submitting a new review form, submit button is disabled 
// to prevent double database submits
$(".review-form").on('submit', function () {
    $(".submit-edit").prop("disabled", true);
});

// Calls the sendmail function for the contact form and prevents the page
// reloading so that a success or failure message can be displayed
$(".contact-form").on('submit', function (event) {
    addLoadingSpinner(".submit-contact");
    $(".contact-error").html("");
    sendMail(this);
    event.preventDefault();
});

// Calls the addLoadingSpinner function when a review form is submitted
$(".review-form").on('submit', function () {
    addLoadingSpinner(".submit-edit");
});

// Calls the addLoadingSpinner function when a search is submitted
$("#search-api").on('submit', function () {
    addLoadingSpinner(".search-api-button");
});

// Calls the addLoadingSpinner function when a fliter search is submitted
// on the reviews page
$("#browse-reviews-form").on('submit', function () {
    addLoadingSpinner(".filter-reviews");
});

// Calls the c when a fliter search is submitted
// on the my_reviews page
$("#user-reviews-form").on('submit', function () {
    addLoadingSpinner(".filter-reviews");
});

// Call the goBack function which goes back to the previous page in history
$(".go-back").click(goBack);

// Calls the addLoadingSpinner function when the confirm-delete button
// or all-reviews-btn or review-this or edit-review or next-button or
// previous-button buttons are clicked
$(".confirm-delete, .all-reviews-btn, .review-this, .edit-review,\
    .next-button, .previous-button").click(function() {
    addLoadingSpinner(this);
});

// Puts a loading spinner on the title when a review is clicked on the browse
// reviews or my_reviews pages
$(".index-card").on('click', function () {
    $(this).find(".card-title").html("<span class='spinner-border spinner-border-sm' role='status' aria-hidden='true'></span> Loading...");
    $(this).prop("disabled", true);
});

// Add a spinner to the back button
$(".go-back").on('click', function () {
    $(this).html("<span class='spinner-border spinner-border-sm text-warning' role='status' aria-hidden='true'></span>");
    $(this).prop("disabled", true);
});

// Handles modal for confirming deletion of individual reviews
// adapted from bootstrap docs
$(document).on('show.bs.modal', "#reviewDeleteModal", function (event) {
    // Button that triggered the modal
    let button = event.relatedTarget;
    // Extract info from data-bs-* attributes
    let recipient = $(button).attr('data-bs-review');
    $("#reviewConfirmDelete").attr("href", recipient);
});
