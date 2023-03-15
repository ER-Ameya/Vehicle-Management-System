$(document).ready(function() {
    $('form').submit(function(event) {
      event.preventDefault(); // Prevent the form from submitting normally
      $.ajax({
        url: $(this).attr('action'), // Get the form action URL
        method: $(this).attr('method'), // Get the form submission method
        data: $(this).serialize(), // Serialize the form data
        success: function(response) {
          // Handle the form submission success response
          alert('Vehicle added successfully!');
          location.reload(); // Reload the page to show the updated vehicle list
        },
        error: function(xhr, status, error) {
          // Handle the form submission error response
          alert('An error occurred while adding the vehicle: ' + error);
        }
      });
    });
  });
  