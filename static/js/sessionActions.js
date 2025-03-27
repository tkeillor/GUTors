// sessionActions.js
document.addEventListener('DOMContentLoaded', function() {
    // Find all containers with the session-actions class
    var actionContainers = document.querySelectorAll('.session-actions');
    
    // For each container, set up the review/edit buttons based on data attributes
    actionContainers.forEach(function(container) {
      var sessionId = container.getAttribute('data-session-id');
      var isReviewed = container.getAttribute('data-is-reviewed') === 'true';
      var reviewUrl = container.getAttribute('data-review-url');
      
      if (isReviewed) {
        container.innerHTML = `
          <div class="alert alert-info">
            You've already reviewed this session
          </div>
          <a href="${reviewUrl}" class="btn btn-outline-uni-blue">Edit Review</a>
        `;
      } else {
        container.innerHTML = `
          <a href="${reviewUrl}" class="btn btn-uni-blue">Write a Review</a>
        `;
      }
    });
  });