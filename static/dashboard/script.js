// Utility function to get CSRF token from the DOM
function getCSRFToken() {
    const tokenElement = document.querySelector('meta[name="csrf-token"]');
    return tokenElement ? tokenElement.getAttribute('content') : '';
}

function control(server, action) {
    const csrfToken = getCSRFToken();  // Get the CSRF token

    fetch(`/dashboard/${action}/${server}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',  // Optional if you send JSON
            'X-CSRFToken': csrfToken  // Add CSRF token to the request headers
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert(data.message);  // Show success message
        } else if (data.error) {
            alert(data.error);  // Show error message
        }
    })
    .catch(error => alert('Error: ' + error));
}
