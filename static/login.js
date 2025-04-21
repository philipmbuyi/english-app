// Add this to your login.js or a script tag in your template
document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.querySelector('form[action="/login"]');
    
    loginForm.addEventListener('submit', function(e) {
        // The modal will be automatically closed when the page redirects 
        // after a successful login
        
        // Optional: Show a loading spinner
        const submitButton = this.querySelector('button[type="submit"]');
        submitButton.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Logging in...';
        submitButton.disabled = true;
    });
});