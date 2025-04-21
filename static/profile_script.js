document.addEventListener('DOMContentLoaded', function() {
    // Initialize profile progress chart
    initializeProgressChart();
    
    // Set up profile form submission
    const profileForm = document.getElementById('profile-form');
    if (profileForm) {
        profileForm.addEventListener('submit', function(e) {
            e.preventDefault();
            updateProfile();
        });
    }
    
    // Set up password change functionality
    const changePasswordBtn = document.getElementById('change-password-btn');
    if (changePasswordBtn) {
        changePasswordBtn.addEventListener('click', function() {
            const passwordModal = new bootstrap.Modal(document.getElementById('passwordModal'));
            passwordModal.show();
        });
    }
    
    const savePasswordBtn = document.getElementById('save-password');
    if (savePasswordBtn) {
        savePasswordBtn.addEventListener('click', function() {
            changePassword();
        });
    }
});

function initializeProgressChart() {
    const ctx = document.getElementById('moduleProgressChart');
    if (!ctx) return;
    
    // Fetch user progress data from the server
    fetch('/api/user/progress')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok: ' + response.status);
            }
            return response.json();
        })
        .then(data => {
            // Create chart with the returned data
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: data.module_names || ['Grammar', 'Writing', 'Pronunciation', 'Conversation', 'Reading'],
                    datasets: [{
                        label: 'Module Completion Percentage',
                        data: data.completion_percentages || [85, 65, 40, 30, 20],
                        backgroundColor: 'rgba(52, 152, 219, 0.5)',
                        borderColor: 'rgba(52, 152, 219, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true,
                            max: 100,
                            title: {
                                display: true,
                                text: 'Completion Percentage'
                            }
                        }
                    }
                }
            });
        })
        .catch(error => {
            console.error('Error loading progress data:', error);
            
            // Fallback to sample data
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: ['Grammar', 'Writing', 'Pronunciation', 'Conversation', 'Reading'],
                    datasets: [{
                        label: 'Module Completion Percentage',
                        data: [85, 65, 40, 30, 20],
                        backgroundColor: 'rgba(52, 152, 219, 0.5)',
                        borderColor: 'rgba(52, 152, 219, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true,
                            max: 100,
                            title: {
                                display: true,
                                text: 'Completion Percentage'
                            }
                        }
                    }
                }
            });
        });
}

function updateProfile() {
    const email = document.getElementById('email').value;
    const phone = document.getElementById('phone').value;
    const languageLevel = document.getElementById('language_level').value;
    
    // Prepare data to send
    const data = {
        email: email,
        phone: phone,
        language_level: languageLevel
    };
    
    // Send data to server
    fetch('/api/user/profile', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok: ' + response.status);
        }
        return response.json();
    })
    .then(data => {
        // Show success message
        const alertHTML = `
            <div class="alert alert-success alert-dismissible fade show" role="alert">
                Profile updated successfully!
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
        `;
        
        // Insert alert before the form
        document.getElementById('profile-form').insertAdjacentHTML('beforebegin', alertHTML);
    })
    .catch(error => {
        console.error('Error updating profile:', error);
        
        // Show error message
        const alertHTML = `
            <div class="alert alert-danger alert-dismissible fade show" role="alert">
                Failed to update profile: ${error.message}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
        `;
        
        // Insert alert before the form
        document.getElementById('profile-form').insertAdjacentHTML('beforebegin', alertHTML);
    });
}

function changePassword() {
    const currentPassword = document.getElementById('current-password').value;
    const newPassword = document.getElementById('new-password').value;
    const confirmPassword = document.getElementById('confirm-password').value;
    
    // Check if passwords match
    if (newPassword !== confirmPassword) {
        document.getElementById('password-error').textContent = 'New passwords do not match';
        document.getElementById('password-error').style.display = 'block';
        return;
    }
    
    // Hide any previous error
    document.getElementById('password-error').style.display = 'none';
    
    // Prepare data to send
    const data = {
        current_password: currentPassword,
        new_password: newPassword
    };
    
    // Send data to server
    fetch('/api/user/change-password', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok: ' + response.status);
        }
        return response.json();
    })
    .then(data => {
        // Hide the modal
        const passwordModal = bootstrap.Modal.getInstance(document.getElementById('passwordModal'));
        passwordModal.hide();
        
        // Show success message
        const alertHTML = `
            <div class="alert alert-success alert-dismissible fade show" role="alert">
                Password changed successfully!
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
        `;
        
        // Insert alert at the top of the profile container
        document.querySelector('.profile-container').insertAdjacentHTML('afterbegin', alertHTML);
        
        // Clear the form
        document.getElementById('password-form').reset();
    })
    .catch(error => {
        console.error('Error changing password:', error);
        
        // Show error in the modal
        document.getElementById('password-error').textContent = `Failed to change password: ${error.message}`;
        document.getElementById('password-error').style.display = 'block';
    });
}