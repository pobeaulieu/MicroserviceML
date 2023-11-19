// Wait for the DOM content to be fully loaded


function submitForm(event) {
    event.preventDefault();

    var form = document.getElementById('main_form')
    var mainForm = new FormData(document.getElementById('main_form'));

    if (!form.checkValidity()) {
        alert('Please provide Github url and call graph!');
        return
    } 

    // Show modal
    document.getElementById('modal').style.display = 'flex';

      
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

