function submitForm(event) {
    event.preventDefault();

    // Clear previous status
    document.getElementById('status').innerHTML = '';

    // Show spinner
    document.getElementById('spinner').style.display = 'block';

    // Get form data
    var formData = new FormData(document.getElementById('cloneForm'));

    // Send asynchronous POST request
    fetch('/pipeline', {
        method: 'POST',
        body: formData
    })
    .then(response => response.text())
    .then(data => {
        // Hide spinner
        document.getElementById('spinner').style.display = 'none';
        
        // Update status
        document.getElementById('status').innerHTML = data;
    })
    .catch(error => console.error('Error:', error));
}

document.addEventListener("DOMContentLoaded", function() {
    var socket = io.connect('http://' + document.domain + ':' + location.port);

    socket.on('update', function(data) {
        // Update status
        document.getElementById('status').innerHTML = data.message;
        
        // Hide spinner
        document.getElementById('spinner').style.display = 'none';
    });
});
