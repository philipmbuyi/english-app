document.addEventListener('DOMContentLoaded', function() {
    // Load the student list when the page loads
    loadStudentList();
    
    // Navigation functionality
    const navLinks = document.querySelectorAll('.dashboard-container nav ul li a');
    const sections = document.querySelectorAll('.dashboard-section');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Remove active class from all links
            navLinks.forEach(l => l.classList.remove('active'));
            
            // Add active class to current link
            this.classList.add('active');
            
            // Hide all sections
            sections.forEach(section => {
                section.style.display = 'none';
            });
            
            // Show the selected section
            const sectionId = this.getAttribute('data-section');
            document.getElementById(sectionId).style.display = 'block';
        });
    });
    
    // Progress tracking chart
    const progressCtx = document.getElementById('progressChart');
    let progressChart;
    
    document.getElementById('load-progress').addEventListener('click', function() {
        const studentId = document.getElementById('student-progress-id').value;
        
        if (!studentId) {
            alert('Please enter a student ID');
            return;
        }
        
        // Sample data - in a real app, you would fetch this from your backend
        const progressData = {
            labels: ['Grammar', 'Writing', 'Pronunciation', 'Conversation', 'Reading'],
            datasets: [{
                label: 'Completion Percentage',
                data: [100, 85, 70, 40, 20],
                backgroundColor: 'rgba(52, 152, 219, 0.5)',
                borderColor: 'rgba(52, 152, 219, 1)',
                borderWidth: 1
            }]
        };
        
        if (progressChart) {
            progressChart.destroy();
        }
        
        progressChart = new Chart(progressCtx, {
            type: 'bar',
            data: progressData,
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
    
    // Test scheduling form
    document.getElementById('test-schedule-form').addEventListener('submit', function(e) {
        e.preventDefault();
        
        const studentId = document.getElementById('student-id').value;
        const testName = document.getElementById('test-name').value;
        const testDate = document.getElementById('test-date').value;
        const testTime = document.getElementById('test-time').value;
        
        if (!studentId || !testName || !testDate || !testTime) {
            alert('Please fill all fields');
            return;
        }
        
        // In a real app, you would send this data to your backend
        document.getElementById('test-schedule-feedback').innerHTML = 
            `<div class="alert alert-success">Test "${testName}" scheduled successfully for Student ID: ${studentId} on ${testDate} at ${testTime}</div>`;
            
        // Clear form
        this.reset();
    });
    
    // Marks management
    document.getElementById('load-marks').addEventListener('click', function() {
        const studentId = document.getElementById('student-marks-id').value;
        
        if (!studentId) {
            alert('Please enter a student ID');
            return;
        }
        
        // Sample data - in a real app, you would fetch this from your backend
        const marksData = [
            { testName: 'Grammar Test', mark: 85 },
            { testName: 'Vocabulary Quiz', mark: 92 },
            { testName: 'Reading Comprehension', mark: 78 },
            { testName: 'Listening Test', mark: 88 },
            { testName: 'Speaking Assessment', mark: 82 }
        ];
        
        const tableBody = document.getElementById('marks-table-body');
        tableBody.innerHTML = '';
        
        marksData.forEach(item => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${item.testName}</td>
                <td>${item.mark}</td>
                <td>
                    <button class="edit-mark" data-test="${item.testName}">Edit</button>
                </td>
            `;
            tableBody.appendChild(row);
        });
        
        // Add event listeners for edit buttons
        document.querySelectorAll('.edit-mark').forEach(button => {
            button.addEventListener('click', function() {
                const testName = this.getAttribute('data-test');
                const newMark = prompt(`Enter new mark for ${testName}:`, 
                    marksData.find(item => item.testName === testName).mark);
                
                if (newMark !== null) {
                    const markValue = parseInt(newMark);
                    if (isNaN(markValue) || markValue < 0 || markValue > 100) {
                        alert('Please enter a valid mark between 0 and 100');
                        return;
                    }
                    
                    // In a real app, you would send this to your backend
                    this.closest('tr').cells[1].textContent = markValue;
                    
                    document.getElementById('marks-management-feedback').innerHTML = 
                        `<div class="alert alert-success">Mark updated successfully for ${testName}</div>`;
                }
            });
        });
    });
});

function loadStudentList() {
    fetch('/api/students')
        .then(response => {
            if (response.status === 403) {
                // Session expired or unauthorized
                throw new Error('Session expired. Please log in again.');
            }
            if (!response.ok) {
                throw new Error('Network response was not ok: ' + response.status);
            }
            return response.json();
        })
        .then(students => {
            console.log("Received students data:", students); // Add debugging
            displayStudents(students);
        })
        .catch(error => {
            console.error('Error loading student list:', error);
            
            // Check if it's a session error
            if (error.message.includes('Session expired')) {
                document.getElementById('student-table-container').innerHTML = 
                    `<div class="alert alert-danger">${error.message} <a href="/login">Login again</a></div>`;
                return;
            }
            
            // Fallback to sample data for other errors
            const sampleStudents = [
                {user_id: 1, username: "john_doe", email: "john@example.com", phone: "123-456-7890", registration_date: "2023-04-15T10:30:00"},
                {user_id: 2, username: "jane_smith", email: "jane@example.com", phone: "987-654-3210", registration_date: "2023-05-20T14:45:00"},
                {user_id: 3, username: "alice_johnson", email: "alice@example.com", phone: "555-123-4567", registration_date: "2023-06-10T09:15:00"}
            ];
            
            displayStudents(sampleStudents);
            
            document.getElementById('student-table-container').innerHTML += 
                `<div class="alert alert-warning">Using sample data. API error: ${error.message}</div>`;
        });
}

function displayStudents(students) {
    const tableBody = document.getElementById('student-table-body');
    tableBody.innerHTML = ''; // Clear existing rows
    
    students.forEach(student => {
        const row = document.createElement('tr');
        
        row.innerHTML = `
            <td>${student.user_id}</td>
            <td>${student.username}</td>
            <td>${student.email || 'N/A'}</td>
            <td>${student.phone || 'N/A'}</td>
            <td>••••••••</td>
            <td><button class="view-details" data-id="${student.user_id}">View Details</button></td>
        `;
        
        tableBody.appendChild(row);
    });
    
    // Set up view details buttons
    document.querySelectorAll('.view-details').forEach(button => {
        button.addEventListener('click', function() {
            const studentId = this.getAttribute('data-id');
            viewStudentDetails(studentId);
        });
    });
}

function viewStudentDetails(studentId) {
    fetch(`/api/students/${studentId}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok: ' + response.status);
            }
            return response.json();
        })
        .then(student => {
            // Create modal to display student details
            const modal = document.createElement('div');
            modal.className = 'modal fade show';
            modal.style.display = 'block';
            modal.setAttribute('tabindex', '-1');
            modal.setAttribute('role', 'dialog');
            modal.setAttribute('aria-modal', 'true');
            
            modal.innerHTML = `
                <div class="modal-dialog" role="document">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">Student Details</h5>
                            <button type="button" class="btn-close close-modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">
                            <p><strong>ID:</strong> ${student.user_id}</p>
                            <p><strong>Username:</strong> ${student.username}</p>
                            <p><strong>Email:</strong> ${student.email || 'N/A'}</p>
                            <p><strong>Phone:</strong> ${student.phone || 'N/A'}</p>
                            <p><strong>Registration Date:</strong> ${new Date(student.registration_date).toLocaleString()}</p>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary close-modal">Close</button>
                        </div>
                    </div>
                </div>
            `;
            
            document.body.appendChild(modal);
            
            // Add backdrop
            const backdrop = document.createElement('div');
            backdrop.className = 'modal-backdrop fade show';
            document.body.appendChild(backdrop);
            
            // Store original active element to restore focus later
            const previousActiveElement = document.activeElement;
            
            // Focus the first focusable element in the modal
            const focusableElements = modal.querySelectorAll('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])');
            if (focusableElements.length) {
                focusableElements[0].focus();
            }
            
            // Handle keyboard accessibility
            modal.addEventListener('keydown', function(e) {
                // Close on escape key
                if (e.key === 'Escape') {
                    closeModal();
                }
                
                // Trap focus inside modal
                if (e.key === 'Tab') {
                    if (focusableElements.length === 0) return;
                    
                    const firstElement = focusableElements[0];
                    const lastElement = focusableElements[focusableElements.length - 1];
                    
                    if (e.shiftKey && document.activeElement === firstElement) {
                        e.preventDefault();
                        lastElement.focus();
                    } else if (!e.shiftKey && document.activeElement === lastElement) {
                        e.preventDefault();
                        firstElement.focus();
                    }
                }
            });
            
            // Close modal functionality
            const closeModal = function() {
                document.body.removeChild(modal);
                document.body.removeChild(backdrop);
                document.body.classList.remove('modal-open');
                
                // Restore focus to the element that had it before the modal was opened
                if (previousActiveElement) {
                    previousActiveElement.focus();
                }
                loadStudentList();
            };
            
            // Add event listeners to close buttons
            modal.querySelectorAll('.close-modal').forEach(button => {
                button.addEventListener('click', closeModal);
            });
            
            // Also close when clicking on backdrop
            backdrop.addEventListener('click', closeModal);
        })
        .catch(error => {
            console.error('Error fetching student details:', error);
            alert(`Error loading student details: ${error.message}`);
        });
}