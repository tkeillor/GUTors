// bookSession.js
document.addEventListener('DOMContentLoaded', function() {
    // Find all booking buttons
    const bookButtons = document.querySelectorAll('.book-session-btn');
    
    // Add click event listener to each button
    bookButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            const sessionId = this.getAttribute('data-session-id');
            bookSession(sessionId, this);
        });
    });
    
    // Function to handle booking via AJAX
    function bookSession(sessionId, button) {
        // Disable button to prevent multiple clicks
        button.disabled = true;
        button.textContent = 'Booking...';
        
        // Get CSRF token
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        
        // Create form data
        const formData = new FormData();
        formData.append('submit', 'Book Session');
        
        // Send AJAX request
        fetch(`/GUTors/session/${sessionId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
            },
            body: formData,
            credentials: 'same-origin'
        })
        .then(response => {
            if (response.ok) {
                // Success - update UI
                button.textContent = 'Booked!';
                button.classList.remove('btn-uni-blue');
                button.classList.add('btn-success');
                
                // Refresh page after a short delay
                setTimeout(() => {
                    window.location.reload();
                }, 1500);
            } else {
                // Error - show message
                button.textContent = 'Error booking';
                button.classList.remove('btn-uni-blue');
                button.classList.add('btn-danger');
                
                // Re-enable after a delay
                setTimeout(() => {
                    button.disabled = false;
                    button.textContent = 'Try Again';
                    button.classList.remove('btn-danger');
                    button.classList.add('btn-uni-blue');
                }, 3000);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            button.textContent = 'Error';
            button.disabled = false;
            button.classList.remove('btn-uni-blue');
            button.classList.add('btn-danger');
        });
    }
});