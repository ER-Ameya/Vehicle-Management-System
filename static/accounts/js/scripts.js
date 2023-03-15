// scripts.js

// When the page has finished loading, execute this code
$(document).ready(function() {
    // Add a submit event listener to the login form
    $('#login-form').submit(function(event) {
      // Get the values of the username and password fields
      var username = $('#username').val();
      var password = $('#password').val();
  
      // If either field is empty, show an error message and prevent the form from being submitted
      if (!username || !password) {
        event.preventDefault(); // Prevent the form from being submitted
        $('#error-message').text('Please enter your username and password').show();
      }
    });
  });
  