// Scrolls window to top on page load
$(document).ready(function () {
    window.scroll(0, 0);
});

// Example starter JavaScript for disabling form submissions if there are invalid fields
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

function goBack() {
    window.history.back();
}

$(".go-back").click(goBack)

$(".call-delete").click(function() {
    $(this).addClass("d-none");
    $(this).siblings(".confirm-delete").removeClass("d-none");
});

$(".likes").click(function() {
    var val = parseInt($(this).attr("value"));
    console.log(val)
    $(this).prop("disabled", true).html(val+1);
});