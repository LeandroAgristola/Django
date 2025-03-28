// Wait for the DOM content to be fully loaded before executing the script
// Ensures that all elements are available for manipulation

document.addEventListener('DOMContentLoaded', function() {
    // Select the contact form element by its ID
    var form = document.getElementById('contactForm');
    
    // Initialize the loading modal and success message modal using Bootstrap
    var loadingModal = new bootstrap.Modal(document.getElementById('loadingModal'));
    var msjModal = new bootstrap.Modal(document.getElementById('msjModal'));

    // Check if the form exists to avoid errors
    if (form) {
        // Add an event listener for the 'submit' event on the form
        form.addEventListener('submit', function(event) {
            // Prevent the default form submission behavior (e.g., page reload)
            event.preventDefault(); 

            // Gather form data using FormData API
            var formData = new FormData(form);

            // Remove any existing error messages from the form
            document.querySelectorAll('.alert.alert-danger').forEach(function(element) {
                element.remove();
            });

            // Send form data to the server using the Fetch API
            fetch(window.location.href, {
                method: 'POST', // HTTP method for sending form data
                body: formData,  // Form data to be sent
                headers: {
                    // Indicate that the request is an AJAX call
                    'X-Requested-With': 'XMLHttpRequest',
                    // Include CSRF token for security (Django-specific)
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                }
            })
            .then(response => response.json()) // Convert server response to JSON
            .then(data => {
                // Check the status of the response
                if (data.status === 'ok') {
                    // Show the loading modal
                    loadingModal.show();
                    // After a delay, hide the loading modal and show the success message modal
                    setTimeout(() => {
                        loadingModal.hide(); // Hide the loading modal
                        msjModal.show();     // Show the success modal
                        form.reset();        // Reset the form fields
                    }, 1000); // 1-second delay
                } 
                // Handle validation errors returned by the server
                else if (data.status === 'invalid') {
                    console.log('Validation errors:', data.errors);
                    
                    // Parse the JSON-encoded error messages
                    var errors = JSON.parse(data.errors);
                    
                    // Loop through each field with validation errors
                    for (var field in errors) {
                        var errorMessages = errors[field]; // List of error messages for the field

                        // Find the form input element corresponding to the field
                        var fieldElement = document.querySelector('[name=' + field + ']');
                        if (fieldElement) {
                            // Create a new error message container
                            var errorElement = document.createElement('div');
                            errorElement.className = 'alert alert-danger mt-2'; // Bootstrap alert class
                            
                            // Append each error message to the container
                            errorMessages.forEach(function(error) {
                                var errorText = document.createTextNode(error.message);
                                errorElement.appendChild(errorText);
                            });
                            
                            // Add the error message below the corresponding form field
                            fieldElement.parentElement.appendChild(errorElement);
                        }
                    }
                }
            })
            // Handle any unexpected errors that occur during form submission
            .catch(error => {
                console.error('Error sending form:', error); // Log the error to the console
            });
        });
    }
});
