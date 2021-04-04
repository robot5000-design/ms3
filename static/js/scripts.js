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
 * 
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
    $(".submit-contact").prop("disabled", false);
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

$(".call-delete, .delete-genre").click(function () {
    $(this).addClass("invisible");
    $(this).siblings(".confirm-delete, .confirm-genre").removeClass("invisible");
});

$(".review-form").on('submit', function () {
    $(".submit-edit").prop("disabled", true);
});

$(".contact-form").on('submit', function (event) {
    $(".submit-contact").prop("disabled", true);
    sendMail(this);
    event.preventDefault();
});

/**
 * Sends the feedback form values to the emailjs service template
 */
$("#search-api").on('submit', function (event) {
    $.ajax({
        type: 'POST',
        url: '/search',
        data: $("#search-api").serialize(),
        success: function () {
            alert("success")
            event.preventDefault();
        },
        error: function() {
            alert("error")
            console.log("error");
        }
    })

});

/**
 * When the go-back button is clicked the browser returns to the
 * previous page in history
 */
function goBack(event) {
    window.history.back();
    event.preventDefault();
}

// Click Events ###################################################################################

$(".go-back").click(goBack)
