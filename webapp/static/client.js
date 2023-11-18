// Wait for the DOM content to be fully loaded
document.addEventListener('DOMContentLoaded', function () {
    // Find the button element by its ID
    var submitButton = document.getElementById('genms');

    // Add a click event listener to the button
    submitButton.addEventListener('click', function (event) {
        // Call the submitForm function when the button is clicked
        submitForm(event);
    });
});

function submitForm(event) {
    event.preventDefault();

    // Get form data for the main form
    var mainForm = new FormData(document.getElementById('main_form'));

    // Get form data for the optional parameters form
    var optionalParamsForm = new FormData(document.getElementById('optionnal_params'));

    // Append the fields of the optional parameters form to the main form
    for (var pair of optionalParamsForm.entries()) {
        mainForm.append(pair[0], pair[1]);
    }

    // Convert the FormData to a query string
    var queryString = new URLSearchParams(mainForm).toString();

    // Redirect to the /pipeline route with the query string
    window.location.href = '/pipeline?' + queryString;
}

