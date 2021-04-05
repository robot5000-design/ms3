// Scrolls window to top on page load
$(document).ready(function () {
    window.scroll(0, 0);
    //$('#csrf_token').val('ABC');
});

// Regular Functions  ######################################################################

/**
 * Sends the feedback form values to the emailjs service template
 * @param { object } contactForm - feedback form values
 */
function sendMail(contactForm) {
    emailjs.send("service_ceip qpk", "template_7pribcf", {
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
 * 
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
    'use strict'
    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    var forms = document.querySelectorAll('.needs-validation')
    // Loop over them and prevent submission
    Array.prototype.slice.call(forms)
        .forEach(function (form) {
            form.addEventListener('submit', function (event) {
                if (!form.checkValidity()) {
                    event.preventDefault()
                    event.stopPropagation()
                }
                form.classList.add('was-validated')
            }, false)
        })
})()

/**
 * When the go-back button is clicked the browser returns to the
 * previous page in history
 */
function goBack() {
    window.history.back();
}

// Click Events ###################################################################################

// makes the delete process a two step process. Press the call-delete
// button  and the confirm-delete goes from invisible to visible
$(".call-delete, .delete-genre").click(function () {
    $(this).addClass("invisible");
    $(this).siblings(".confirm-delete, .confirm-genre").removeClass("invisible");
});

// On submitting a new review form, submit button is disabled 
// to prevent double database submits
$(".review-form").on('submit', function () {
    $(".submit-edit").prop("disabled", true);
});

function addLoadingSpinner(toThisButton) {
    $(toThisButton).html("<span class='spinner-border spinner-border-sm' role='status' aria-hidden='true'></span> Loading...");
    $(toThisButton).prop("disabled", true);
}

function removeLoadingSpinner(toThisButton, buttonText) {
    $(toThisButton).html(buttonText);
    $(toThisButton).prop("disabled", false);
}

$("#search-api").on('submit', function () {
    addLoadingSpinner(".search-api-button");
});


// Calls the sendmail function for the contact form and prevents the page
// reloading so that a success or failure message can be displayed
$(".contact-form").on('submit', function (event) {
    addLoadingSpinner(".submit-contact");
    $(".contact-error").html("")
    sendMail(this);
    event.preventDefault();
});

$(".review-form").on('submit', function () {
    addLoadingSpinner(".submit-edit");
});

// Call the goBack function which goes back to the previous page in history
$(".go-back").click(goBack)
