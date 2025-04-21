from flask import Flask, render_template, request, redirect, url_for, session, send_file, flash
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import os
import random
import string
from datetime import datetime
from quizzes_population import populate_quizzes
from quizzes import QuizManager
from database import Database
import json
import pymysql
from flask import send_from_directory
from flask import Flask, jsonify
from fpdf import FPDF  # This requires the fpdf library 
from datetime import datetime, timedelta

# Define a constant for certificate storage location
CERTIFICATE_FOLDER = 'static/certificates'
os.makedirs(CERTIFICATE_FOLDER, exist_ok=True)

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['DEBUG'] = True
app.config['CERTIFICATES_FOLDER'] = 'certificates'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)  # Set session timeout

# Initialize database
db = Database()

# Initialize database tables when the app starts
db.init_db()
db.update_quiz_tables() 
populate_quizzes()
quiz_manager = QuizManager(db)



# generate certificate
def generate_certificate(username, module_name, quiz_id, score, total):
    """Generate a PDF certificate for the user"""
    pdf = FPDF()
    pdf.add_page()
    
    # Set up the PDF
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'Certificate of Completion', 0, 1, 'C')
    
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, f'This certifies that {username}', 0, 1, 'C')
    pdf.cell(0, 10, f'has successfully completed the {module_name} module', 0, 1, 'C')
    pdf.cell(0, 10, f'with a score of {score}/{total}', 0, 1, 'C')
    pdf.cell(0, 10, f'Date: {datetime.now().strftime("%B %d, %Y")}', 0, 1, 'C')
    
    # Generate a unique filename
    random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    filename = f"{username}_{module_name}_quiz{quiz_id}_{random_str}.pdf"
    file_path = os.path.join(CERTIFICATE_FOLDER, filename)
    
    # Save the PDF
    pdf.output(file_path)
    
    return filename

    

# function to retrieve use informations 
def get_user_from_json(username=None, user_id=None):
    """Get user information from JSON file by username or user_id"""
    json_file = os.path.join('user_data', 'users.json')
   
    if not os.path.exists(json_file):
        return None
   
    with open(json_file, 'r') as f:
        users = json.load(f)
   
    if username:
        for user in users:
            if user['username'] == username:
                return user
    elif user_id:
        # Convert user_id to int for comparison if it's a string
        user_id_to_check = int(user_id) if isinstance(user_id, str) and user_id.isdigit() else user_id
        for user in users:
            if user['user_id'] == user_id_to_check:
                return user
   
    return None

def save_user_to_json(user_id, username, email, password,phone=''):
    """Save user information to a JSON file"""
    data_dir = 'user_data'
    
    # Create directory if it doesn't exist
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    # File path for the JSON file
    json_file = os.path.join(data_dir, 'users.json')
    
    # Create user data with password hash
    user_data = {
        'user_id': user_id,
        'username': username,
        'email': email,
        'phone': phone,
        'password': password,  # Storing plain password as requested (not recommended in production)
        'password_hash': generate_password_hash(password),
        'registration_date': datetime.now().isoformat()
    }
    
    # Read existing data if file exists
    if os.path.exists(json_file):
        with open(json_file, 'r') as f:
            try:
                users = json.load(f)
            except json.JSONDecodeError:
                users = []
    else:
        users = []
    
    # Add new user data
    users.append(user_data)
    
    # Write back to file
    with open(json_file, 'w') as f:
        json.dump(users, f, indent=4)
    
    print(f"User data saved to {json_file}")

def get_all_users():
    """Get all users from JSON file"""
    json_file = os.path.join('user_data', 'users.json')
   
    if not os.path.exists(json_file):
        print(f"JSON file does not exist: {json_file}")
        return []
   
    try:
        with open(json_file, 'r') as f:
            try:
                users = json.load(f)
                print(f"Successfully loaded {len(users)} users from JSON")
                return users
            except json.JSONDecodeError as e:
                print(f"JSON decode error: {str(e)}")
                return []
    except IOError as e:
        print(f"File I/O error: {str(e)}")
        return []
        
@app.route('/api/students', methods=['GET'])
def api_get_students():
    # Check if user is admin
    if 'is_admin' not in session:
        print("No admin session found")
        return jsonify({"error": "No session", "redirect": "/login"}), 403
    
    if not session['is_admin']:
        print("User is not admin")
        return jsonify({"error": "Unauthorized", "redirect": "/login"}), 403
   
    # Log the request
    print("API request received for students list")
   
    # Get all users from JSON file
    users = get_all_users()
    print(f"Found {len(users)} users in JSON file")
   
    # Return users as JSON
    return jsonify(users)

@app.route('/api/students/<user_id>', methods=['GET'])
def api_get_student_details(user_id):
    # Check if user is admin
    if 'is_admin' not in session or not session['is_admin']:
        return jsonify({"error": "Unauthorized"}), 403
    
    # Get user details from JSON file
    user = get_user_from_json(user_id=user_id)
    
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    return jsonify(user)

@app.route('/')
def home():
    # Create a guest user if none exists
    if 'username' not in session:
        guest_username = db.create_guest_user()
        session['username'] = guest_username
        session['guest'] = True
    
    # Get user data and progress
    user = db.get_user_by_username(session['username'])
    if user:
        user_progress = db.get_user_progress(user['id'])
    else:
        user_progress = {'progress': {}, 'completed_modules': []}
    
    # Get all modules
    modules_data = db.get_all_modules()
    
    return render_template(
        'dashboard.html', 
        modules=modules_data, 
        username=session['username'],
        user=user_progress,
        is_guest=session.get('guest', False)
    )

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('home'))
    
    # Get user data and progress
    user = db.get_user_by_username(session['username'])
    if user:
        user_progress = db.get_user_progress(user['id'])
    else:
        user_progress = {'progress': {}, 'completed_modules': []}
    
    # Get all modules
    modules_data = db.get_all_modules()
    
    return render_template(
        'dashboard.html',
        modules=modules_data,
        username=session['username'],
        is_guest=session.get('guest', False),
        user=user_progress
    )

@app.route('/upgrade_account', methods=['GET', 'POST'])
def upgrade_account():
    print(f"Session data: {session}")  # Debug session data
    
   
    if 'username' not in session or not session.get('guest'):
        print("User is either not logged in or not a guest")
        return redirect(url_for('home'))
   
    if request.method == 'POST':
        print("Processing POST request for account upgrade")
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        
        print(f"Attempting to upgrade account: {username}, {email}")
        
        # For debugging - save form data to JSON regardless of DB success
        try:
            temp_data = {
                'username': username,
                'email': email,
                'attempt_time': datetime.now().isoformat(),
                'guest_username': session.get('username')
            }
            
            data_dir = 'user_data'
            if not os.path.exists(data_dir):
                os.makedirs(data_dir)
                
            debug_file = os.path.join(data_dir, 'registration_attempts.json')
            
            if os.path.exists(debug_file):
                with open(debug_file, 'r') as f:
                    try:
                        attempts = json.load(f)
                    except json.JSONDecodeError:
                        attempts = []
            else:
                attempts = []
                
            attempts.append(temp_data)
            
            with open(debug_file, 'w') as f:
                json.dump(attempts, f, indent=4)
                
            print(f"Debug data saved to {debug_file}")
        except Exception as e:
            print(f"Error saving debug data: {str(e)}")
   
    return render_template('upgrade.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
       
        # Special case for admin
        if username == 'admin' and password == 'church!':
            session['username'] = username
            session['is_admin'] = True
            session['user_id'] = 'admin'  # Add this line
            flash('Welcome, Admin!')
            return redirect(url_for('admin_dashboard'))
        
        # First try database login
        user = db.get_user_by_username(username)
        print(f"Login attempt for user: {username}, found in DB: {user is not None}")
       
        if user and check_password_hash(user['password'], password):
            session['username'] = username
            if user['is_guest']:
                print(f"Setting guest flag for user: {username}")
                session['guest'] = True
            else:
                print(f"User {username} is not a guest")
                session.pop('guest', None)
            return redirect(url_for('home'))
        
        # If database login fails, try JSON file
        json_user = get_user_from_json(username=username)
        print(f"Checking JSON file for user: {username}, found: {json_user is not None}")
        
        if json_user and 'password_hash' in json_user:
            if check_password_hash(json_user['password_hash'], password):
                session['username'] = username
                session.pop('guest', None)  # JSON-stored users are not guests
                return redirect(url_for('home'))
       
        return render_template('login.html', error='Invalid credentials')
   
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form.get('email', '')  # Make email optional
        phone = request.form.get('phone', '')
        
        # Check if username already exists
        existing_user = db.get_user_by_username(username)
        
        # Handle AJAX requests differently
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        if existing_user:
            if is_ajax:
                return jsonify({'success': False, 'message': 'Username already exists'})
            else:
                return render_template('register.html', error='Username already exists')
        
        # Register new user
        try:
            
            db.register_user(username, password, email, phone)
            session['username'] = username
            if is_ajax:
                return jsonify({'success': True, 'redirect': url_for('home')})
            else:
                return redirect(url_for('home'))
                
        except Exception as e:
            print(f"Registration error: {str(e)}")
            if is_ajax:
                return jsonify({'success': False, 'message': f'Registration error: {str(e)}'})
            else:
                return render_template('register.html', error=f'Registration error: {str(e)}')
    
    return render_template('register.html')
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    success = False
    error = None
    
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        newsletter = request.form.get('newsletter') == 'on'
        
        if db.save_contact_form(name, email, subject, message, newsletter):
            success = True
        else:
            error = "Unable to send message. Please try again later."
    
    return render_template('contact.html', success=success, error=error)

@app.route('/resources')
def resources():
    resources_list = db.get_all_resources()
    return render_template('resources.html', resources=resources_list)

@app.route('/resource/<resource_id>')
def resource_detail(resource_id):
    print(f"Fetching resource with ID: {resource_id}")
    resource = db.get_resource_detail(resource_id)
    print(f"Resource retrieved: {resource}")
    
    if not resource:
        flash('Resource not found. Please try a different resource.')
        return redirect(url_for('resources'))
    
    return render_template('resource_detail.html', resource=resource)

@app.route('/module/<module_name>')
def module(module_name):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    module_data = db.get_module_data(module_name)
    if not module_data:
        return redirect(url_for('home'))
    
    lessons = db.get_lessons_for_module(module_data['id'])
    quizzes = db.get_module_quizzes(module_data['id'])
    
    # Format quizzes with their questions
    quizzes_with_questions = {}
    for quiz in quizzes:
        questions = db.get_quiz_questions(quiz['id'])
        quizzes_with_questions[quiz['id']] = {
            'title': quiz['title'],
            'description': quiz.get('description', ''),
            'questions': questions
        }
    
    module_with_content = {
        'title': module_data['title'],
        'lessons': lessons,
        'quizzes': {
            quiz['id']: {
                'title': quiz['title'],
                'description': quiz.get('description', ''),
                'questions': db.get_quiz_questions(quiz['id'])
            }
            for quiz in quizzes  # quizzes from db.get_module_quizzes()
        }
    }
    
    return render_template(
        'module.html',
        module=module_with_content,
        module_name=module_name,
        username=session['username']
    )


@app.route('/lesson/<module_name>/<int:lesson_id>')
def lesson(module_name, lesson_id):
    if 'username' not in session:
        return redirect(url_for('login'))
   
    module_data = db.get_module_data(module_name)
    if not module_data:
        return redirect(url_for('home'))
   
    lesson_data = db.get_lesson_data(module_data['id'], lesson_id)
    if not lesson_data:
        return redirect(url_for('module', module_name=module_name))
   
    # Update user progress to mark that they've viewed this lesson
    user = db.get_user_by_username(session['username'])
    if user:
        db.update_user_progress(user['id'], module_data['id'])
    
    # Get all lessons for this module to determine prev/next
    all_lessons = db.get_lessons_for_module(module_data['id'])
    prev_lesson = None
    next_lesson = None
    
    # Find prev and next lessons
    for i, l in enumerate(all_lessons):
        if l['lesson_number'] == lesson_id:
            if i > 0:
                prev_lesson = all_lessons[i-1]
            if i < len(all_lessons) - 1:
                next_lesson = all_lessons[i+1]
    
    # Get all modules for sidebar reference
    modules = {module_name: module_data}
   
    return render_template(
        'enhanced-lesson.html',  # Correct spelling
        lesson={
            'id': lesson_data['lesson_number'],
            'title': lesson_data['title'],
            'content': lesson_data['content'],
            'progress': 0,  # Add default values for expected properties
            'duration': '15 min',
            'level': 'Beginner',
            'summary': f'Summary of {lesson_data["title"]}',
            'sections': [],  # Empty array for sections
            'key_points': ['Key point 1', 'Key point 2', 'Key point 3'],
            'resources': []
        },
        module_name=module_name,
        module_title=module_data['title'],
        modules=modules,  # Add modules dictionary
        prev_lesson=prev_lesson,
        next_lesson=next_lesson,
        username=session['username'],
        has_quizzes='quizzes' in module_data
    )

@app.route('/module/<module_name>/quiz/<int:quiz_id>', methods=['GET', 'POST'])
def take_quiz(module_name, quiz_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    module_data = db.get_module_data(module_name)
    if not module_data:
        print(f"Module {module_name} not found")
        return redirect(url_for('dashboard'))
    
    print(f"Module ID: {module_data['id']}")

    if request.method == 'POST':
        
        user = db.get_user_by_username(session['username'])
        if not user:
            flash("User not found. Please log in again or if you are admin try quiz as guest")
            return redirect(url_for('login'))

        results = quiz_manager.grade_quiz(
            user['id'],
            module_data['id'],
            quiz_id,
            request.form
        )
        
        if results.get('error'):
            flash(results['error'])
            return redirect(url_for('module', module_name=module_name))
        
        if results['passed']:
            # Generate certificate filename
            random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
            filename = f"{session['username']}_{module_name}_quiz{quiz_id}_{random_str}.pdf"
            
            # Save results
            db.save_quiz_results(
                user['id'],
                module_data['id'],
                results['score'],
                results['total'],
                filename
            )
        
        return render_template(
            'quiz_result.html',
            score=results['score'],
            total=results['total'],
            percentage=results['percentage'],
            module_name=module_name,
            module_title=module_data['title'],
            certificate_path=filename if results['passed'] else None,
            username=session['username'],
            feedback=results['feedback']
        )
    
    # GET request - show the quiz
    quiz = quiz_manager.get_quiz_for_module(module_data['id'], quiz_id)
    print(f"Quiz returned: {quiz}")
    
    if not quiz:
        print("Quiz not found, redirecting")
        flash('Quiz not found')
        return redirect(url_for('module', module_name=module_name))
    
    # Parse options JSON before passing to template**
    for question in quiz['questions']:
        question['options'] = json.loads(question['options'])  # Convert string to list

    print(f"Quiz data after parsing options: {quiz}")
    
    return render_template(
        'quiz.html',
        quiz=quiz,
        module_name=module_name,
        module_title=module_data['title'],
        quiz_id=quiz_id,
        username=session['username']
    )

@app.route('/api/students', methods=['GET'])
def get_students():
    # Check if the user is an admin (you would need to implement this)
    # if not session.get('is_admin', False):
    #     return jsonify({'error': 'Unauthorized'}), 403
        
    # Get all users
    students = get_all_users()
    
    return jsonify(students)

@app.route('/api/students/<string:student_id>', methods=['GET'])
def get_student(student_id):
    # Check if the user is an admin (you would need to implement this)
    # if not session.get('is_admin', False):
    #     return jsonify({'error': 'Unauthorized'}), 403
        
    # Get the student
    student = get_user_from_json(user_id=student_id)
    
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    
    return jsonify(student) 

@app.route('/final-test', methods=['GET', 'POST'])
def final_test():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    user = db.get_user_by_username(session['username'])
    
    if request.method == 'POST':
        test_id = request.form.get('test_id')
        results = quiz_manager.grade_final_test(
            user['id'],
            test_id,
            request.form
        )
        
        return render_template('final_test_results.html', results=results)
    
    # GET request - generate new test
    test = quiz_manager.generate_final_test(user['id'])
    session['current_test_id'] = test['test_id']
    
    return render_template('take_final_test.html', test=test)

@app.route('/download_certificate/<filename>')
def download_certificate(filename):
    # Ensure the user is logged in
    if 'username' not in session:
        return redirect(url_for('login'))
    
    # Basic security check - only allow downloading if filename contains the username
    # or if it's an admin user (you would need to implement admin check)
    is_admin = False  # Replace with your admin check
    if not is_admin and session['username'] not in filename:
        flash('Unauthorized access to certificate')
        return redirect(url_for('dashboard'))
    
    # Check if the file exists
    if not os.path.exists(os.path.join(CERTIFICATE_FOLDER, filename)):
        flash('Certificate not found')
        return redirect(url_for('dashboard'))
    
    # Return the file
    return send_from_directory(CERTIFICATE_FOLDER, filename)

# Add a new route for the admin dashboard
@app.route('/admin')
def admin_dashboard():
    # Check if user is logged in and is admin
    if 'username' not in session or not session.get('is_admin', False):
        flash('You do not have permission to access the admin dashboard')
        return redirect(url_for('home'))
    
    return render_template('admin_dashboard.html')

# profile route

@app.route('/profile')
def profile():
    # Check if user is logged in
    if 'username' not in session:
        flash('Please log in to view your profile')
        return redirect(url_for('login'))
    
    # Get user data
    user = db.get_user_by_username(session['username'])
    if not user:
        user = {}
    
    # Build user data dictionary
    user_data = {
        'username': session['username'],
        'email': user.get('email', session.get('email', '')),
        'phone': user.get('phone', session.get('phone', '')),
        'language_level': user.get('language_level', session.get('language_level', 'beginner')),
        'registration_date': user.get('registration_date', session.get('registration_date', '')),
    }
    
    # Determine user type
    is_admin = session.get('is_admin', False)
    is_guest = session.get('guest', False)
    
    # Get user progress if we have a user
    user_progress = {'progress': {}, 'completed_modules': []}
    if user and 'id' in user:
        try:
            user_progress = db.get_user_progress(user['id'])
        except Exception as e:
            print(f"Error getting user progress: {str(e)}")
    
    # Get modules data
    modules_data = {}
    try:
        modules_data = db.get_all_modules()
    except Exception as e:
        print(f"Error getting modules: {str(e)}")
        # Fallback to hardcoded modules
        modules_data = {
            'grammar': {'title': 'Grammar', 'id': 1, 'lessons': []},
            'writing': {'title': 'Writing', 'id': 2, 'lessons': []},
            'pronunciation': {'title': 'Pronunciation', 'id': 3, 'lessons': []},
            'conversation': {'title': 'Conversation', 'id': 4, 'lessons': []},
            'reading': {'title': 'Reading', 'id': 5, 'lessons': []}
        }
    
    # Add progress info to modules
    modules_with_progress = {}
    for module_name, module_data in modules_data.items():
        is_completed = module_name in user_progress['completed_modules']
        
        modules_with_progress[module_name] = {
            'title': module_data['title'],
            'id': module_data['id'],
            'completed': is_completed,
            'lessons_count': len(module_data.get('lessons', [])),
            'progress_percentage': 100 if is_completed else 0  # You might want to calculate this differently
        }
    
    # Fetch test results - in a real app, you'd get this from your database
    # This is a placeholder - replace with your actual test results query
    test_results = [
        {'name': 'Grammar Quiz 1', 'date': '2024-03-15', 'score': '85%'},
        {'name': 'Vocabulary Test', 'date': '2024-03-20', 'score': '92%'},
        {'name': 'Reading Comprehension', 'date': '2024-03-27', 'score': '78%'}
    ]
    
    return render_template(
        'profile.html',
        user=user_data,
        modules=modules_with_progress,
        test_results=test_results,
        is_admin=is_admin,
        is_guest=is_guest
    )

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('is_admin', None)
    session.pop('user_id', None)
    session.pop('guest', None)
    flash('You have been logged out successfully')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)