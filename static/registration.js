// JavaScript to handle the form submission - place before closing body tag

document.addEventListener('DOMContentLoaded', function() {
  const registrationForm = document.getElementById('registration-form');

  if (registrationForm) {
      registrationForm.addEventListener('submit', function(e) {
          e.preventDefault();

          // Validate passwords match
          const password = document.getElementById('reg-password').value;
          const confirmPassword = document.getElementById('reg-confirm-password').value;
          const errorDiv = document.getElementById('reg-error-message');

          if (password !== confirmPassword) {
              errorDiv.textContent = "Passwords do not match";
              errorDiv.style.display = "block";
              return;
          }

          // Create FormData object
          const formData = new FormData(registrationForm);

          // Remove confirm_password field before sending
          formData.delete('confirm_password');

          // Send form data via fetch API
          fetch(registrationForm.action, {
              method: 'POST',
              body: formData,
              headers: {
                  'X-Requested-With': 'XMLHttpRequest'
              }
          })
          .then(response => response.json())
          .then(data => {
              if (data.success) {
                  // Close modal
                  const modal = bootstrap.Modal.getInstance(document.getElementById('registrationModal'));
                  modal.hide();

                  // Redirect or show success message
                  if (data.redirect) {
                      window.location.href = data.redirect;
                  }
              } else {
                  // Show error message
                  errorDiv.textContent = data.message || 'Registration failed. Please try again.';
                  errorDiv.style.display = "block";
              }
          })
          .catch(error => {
              console.error('Error:', error);
              errorDiv.textContent = 'An error occurred during registration. Please try again.';
              errorDiv.style.display = "block";
          });
      });
  }
});
