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

/*
function populateLogInModal() {
    $(".modal-content").html(
        `<div class="modal-header">
            <h5 class="modal-title" id="logInModalLabel">Log-In</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
            <form class="needs-validation" action="{{ url_for('login') }}" method="POST" novalidate>
                <div class="mb-3">
                    <label for="username" class="form-label">Username</label>
                    <input id="username" name="username" type="text" class="form-control" minlength="5"
                        pattern="^[a-zA-Z0-9]{5,15}$" maxlength="15" required>
                    <span class="invalid-feedback">must be 5-15 alphanumeric characters (no spaces)</span>
                </div>
                <div class="mb-5">
                    <label for="password" class="form-label">Password</label>
                    <input id="password" name="password" type="password" class="form-control" minlength="5"
                        pattern="^[a-zA-Z0-9]{5,15}$" maxlength="15" required>
                    <span class="invalid-feedback">must be 5-15 alphanumeric characters (no spaces)</span>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                    <button type="submit" class="btn btn-success">Log-In</button>
                </div>
            </form>
            <div>
                <span><a href="#" id="show-register" class="show-register">No Account? Register Here</a></span>
            </div>
        </div>`
    );
}

function populateConfirmModal() {
    $(".modal-content").html(
        `<div class="modal-header">
            <h5 class="modal-title" id="confirmModalLabel">Confirm Delete</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
            <div class="">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                <a href="{{ url_for('delete_review', tmdb_id=movie.tmdb_id) }}"
                    class="btn btn-danger confirm-delete">Delete Review
                </a>
            </div>
        </div>`
    );
}

//$(".confirm-delete").on("click", populateLogInModal);*/

$(".call-delete").click(function() {
    $(".call-delete").addClass("d-none")
    $(".confirm-delete").removeClass("d-none")
})