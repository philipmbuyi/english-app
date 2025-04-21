// enhanced-lesson.js
document.addEventListener('DOMContentLoaded', function() {
    // Smooth scrolling for anchor links
    document.querySelectorAll('.lesson-sections a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 20,
                    behavior: 'smooth'
                });
                
                // Update active state in navigation
                document.querySelectorAll('.lesson-sections .nav-link').forEach(link => {
                    link.classList.remove('active');
                });
                this.classList.add('active');
            }
        });
    });
    
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Word counter for writing exercise
    const writingTextarea = document.getElementById('writing-response');
    const wordCounter = document.getElementById('word-counter');
    
    if (writingTextarea && wordCounter) {
        writingTextarea.addEventListener('input', function() {
            const text = this.value.trim();
            const wordCount = text ? text.split(/\s+/).length : 0;
            wordCounter.textContent = wordCount;
            
            // Visual feedback
            if (wordCount > 100) {
                wordCounter.classList.add('text-danger');
            } else {
                wordCounter.classList.remove('text-danger');
            }
        });
    }
    
    // Grammar exercise check answers
    const checkAnswersBtn = document.querySelector('.check-answers');
    if (checkAnswersBtn) {
        checkAnswersBtn.addEventListener('click', function() {
            const inputs = document.querySelectorAll('.exercise-input');
            inputs.forEach(input => {
                const feedbackContainer = input.closest('.exercise-item').querySelector('.feedback-container');
                feedbackContainer.style.display = 'block';
            });
        });
    }
    
    // Show answers button
    const showAnswersBtn = document.querySelector('.show-answers');
    if (showAnswersBtn) {
        showAnswersBtn.addEventListener('click', function() {
            const inputs = document.querySelectorAll('.exercise-input');
            const answers = ['goes', 'are watching', 'studied']; // Sample answers
            
            inputs.forEach((input, index) => {
                if (index < answers.length) {
                    input.value = answers[index];
                    input.classList.add('is-valid');
                }
                
                const feedbackContainer = input.closest('.exercise-item').querySelector('.feedback-container');
                feedbackContainer.style.display = 'block';
            });
        });
    }
    
    // Pronunciation recording simulation
    const recordButtons = document.querySelectorAll('.record-button');
    recordButtons.forEach(button => {
        button.addEventListener('click', function() {
            const container = this.closest('.record-container');
            const statusContainer = container.querySelector('.recording-status');
            const timerElement = statusContainer.querySelector('.timer');
            
            // Toggle recording state
            if (this.classList.contains('recording')) {
                // Stop recording
                this.classList.remove('recording');
                this.innerHTML = '<i class="fas fa-microphone"></i> Record Your Voice';
                statusContainer.style.display = 'none';
                clearInterval(this.timerInterval);
                
                // Show success message (simulated)
                const successMessage = document.createElement('div');
                successMessage.className = 'alert alert-success mt-2';
                successMessage.innerHTML = '<i class="fas fa-check-circle"></i> Recording saved! Our AI will analyze your pronunciation.';
                container.appendChild(successMessage);
                
                // Remove message after 5 seconds
                setTimeout(() => {
                    successMessage.remove();
                }, 5000);
            } else {
                // Start recording
                this.classList.add('recording');
                this.innerHTML = '<i class="fas fa-stop-circle"></i> Stop Recording';
                statusContainer.style.display = 'flex';
                
                // Simulate timer
                let seconds = 0;
                this.timerInterval = setInterval(() => {
                    seconds++;
                    timerElement.textContent = seconds;
                    
                    // Auto-stop after 10 seconds
                    if (seconds >= 10) {
                        this.click();
                    }
                }, 1000);
            }
        });
    });
    
    // Mark lesson as complete
    const markCompleteBtn = document.querySelector('.mark-complete');
    if (markCompleteBtn) {
        markCompleteBtn.addEventListener('click', function(e) {
            e.preventDefault();
            this.innerHTML = '<i class="fas fa-check-circle"></i> Completed!';
            this.classList.remove('btn-outline-primary');
            this.classList.add('btn-success');
            
            // Update progress (this would typically be an API call)
            const progressBar = document.querySelector('.progress-bar');
            if (progressBar) {
                progressBar.style.width = '100%';
                progressBar.textContent = '100%';
            }
            
            // Update sidebar navigation
            const navLinks = document.querySelectorAll('.lesson-sections .nav-link');
            navLinks.forEach(link => {
                link.classList.add('completed');
                const icon = link.querySelector('i');
                if (icon) {
                    icon.className = 'fas fa-check-circle';
                }
            });
        });
    }
    
    // Simulate audio playback for pronunciation
    const audioButtons = document.querySelectorAll('.play-audio');
    audioButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Visual feedback
            const originalText = this.innerHTML;
            this.innerHTML = '<i class="fas fa-volume-up fa-spin"></i> Playing...';
            this.disabled = true;
            
            // Reset after "playback"
            setTimeout(() => {
                this.innerHTML = originalText;
                this.disabled = false;
            }, 1500);
        });
    });
});