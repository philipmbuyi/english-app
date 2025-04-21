import pymysql
from pymysql.cursors import DictCursor
from werkzeug.security import generate_password_hash, check_password_hash
import random
import string
import os
print("Loading database.py")
class Database:
    def __init__(self):
        self.host = os.getenv('DB_HOST', 'localhost')
        self.user = os.getenv('DB_USER', 'root')
        self.password = os.getenv('DB_PASSWORD', '')
        self.db = os.getenv('DB_NAME', 'mysql')
        self.port = int(os.getenv('DB_PORT', 3306))
        self.charset = 'utf8mb4'
        self.cursorclass = DictCursor

    def get_connection(self):
        return pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            db=self.db,
            port=self.port,
            charset=self.charset,
            cursorclass=self.cursorclass,
            ssl={"ssl": {}}  # Aiven requires SSL
        )

    def init_db(self):
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                # Create users table
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    email VARCHAR(100),
                    is_guest BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """)
                
                # Create modules table
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS modules (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(50) UNIQUE NOT NULL,
                    title VARCHAR(100) NOT NULL
                )
                """)
                
                # Create lessons table
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS lessons (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    module_id INT NOT NULL,
                    lesson_number INT NOT NULL,
                    title VARCHAR(100) NOT NULL,
                    content TEXT NOT NULL,
                    FOREIGN KEY (module_id) REFERENCES modules(id) ON DELETE CASCADE
                )
                """)
                
                # Create user_progress table
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_progress (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    module_id INT NOT NULL,
                    completed BOOLEAN DEFAULT FALSE,
                    completion_date TIMESTAMP NULL,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                    FOREIGN KEY (module_id) REFERENCES modules(id) ON DELETE CASCADE,
                    UNIQUE KEY user_module (user_id, module_id)
                )
                """)
                
                # Create certificates table
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS certificates (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    module_id INT NOT NULL,
                    score INT NOT NULL,
                    total_questions INT NOT NULL,
                    filename VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                    FOREIGN KEY (module_id) REFERENCES modules(id) ON DELETE CASCADE
                )
                """)
                self.update_quiz_tables()
                # Insert module data if modules table is empty
                cursor.execute("SELECT COUNT(*) as count FROM modules")
                count = cursor.fetchone()['count']
                
                if count == 0:
                    # Insert modules
                    modules_data = [
                        ('grammar', 'Grammar Fundamentals'),
                        ('writing', 'Essay Writing Skills'),
                        ('pronunciation', 'Pronunciation Workshop'),
                        ('conversation', 'Conversational English'),
                        ('reading', 'Reading Comprehension'),
                        ('business', 'Business English'),
                        ('music', 'English Through Music'),
                        ('culture', 'Cultural Studies')
                    ]
                    
                    cursor.executemany(
                        "INSERT INTO modules (name, title) VALUES (%s, %s)",
                        modules_data
                    )
                    
                    # Get module IDs
                    cursor.execute("SELECT id, name FROM modules")
                    module_ids = {row['name']: row['id'] for row in cursor.fetchall()}
                    
                    # Insert lessons for each module
                    lessons_data = []
                    
                    # Grammar lessons
                    lessons_data.extend([
                        (module_ids['grammar'], 1, 'Parts of Speech', 'Learn about nouns, verbs, adjectives, and more.'),
                        (module_ids['grammar'], 2, 'Sentence Structure', 'Understand how to build grammatically correct sentences.')
                    ])
                    
                    # Writing lessons
                    lessons_data.extend([
                        (module_ids['writing'], 1, 'Introduction to Essay Writing', 'Basics of crafting a compelling essay.'),
                        (module_ids['writing'], 2, 'Argument Development', 'How to create strong arguments in your writing.')
                    ])
                    
                    # Pronunciation lessons
                    lessons_data.extend([
                        (module_ids['pronunciation'], 1, 'Vowel Sounds', 'Master the different vowel pronunciations.'),
                        (module_ids['pronunciation'], 2, 'Consonant Clusters', 'Practice challenging consonant combinations.')
                    ])
                    
                    # Conversation lessons
                    lessons_data.extend([
                        (module_ids['conversation'], 1, 'Everyday Dialogues', 'Learn common conversational patterns.'),
                        (module_ids['conversation'], 2, 'Idioms and Expressions', 'Understand and use English idioms.')
                    ])
                    
                    # Reading lessons
                    lessons_data.extend([
                        (module_ids['reading'], 1, 'Skimming and Scanning', 'Techniques for efficient reading.'),
                        (module_ids['reading'], 2, 'Analyzing Texts', 'Deep comprehension strategies.')
                    ])
                    
                    # Business lessons
                    lessons_data.extend([
                        (module_ids['business'], 1, 'Professional Communication', 'Email and meeting language.'),
                        (module_ids['business'], 2, 'Business Vocabulary', 'Key terms and expressions.')
                    ])
                    
                    # Music lessons
                    lessons_data.extend([
                        (module_ids['music'], 1, 'Lyric Interpretation', 'Understanding song meanings.'),
                        (module_ids['music'], 2, 'Musical Vocabulary', 'Music-related English terms.')
                    ])
                    
                    # Culture lessons
                    lessons_data.extend([
                        (module_ids['culture'], 1, 'English-Speaking Countries', 'Explore cultural backgrounds.'),
                        (module_ids['culture'], 2, 'Social Customs', 'Understanding cultural norms.')
                    ])
                    
                    cursor.executemany(
                        "INSERT INTO lessons (module_id, lesson_number, title, content) VALUES (%s, %s, %s, %s)",
                        lessons_data
                    )
                    
                    conn.commit()
        finally:
            conn.close()       


    def get_quiz_data(self, module_id, quiz_id):
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                SELECT * FROM quizzes 
                WHERE module_id = %s AND id = %s  # Changed from quiz_number to id
                """, (module_id, quiz_id))
                return cursor.fetchone()
        finally:
            conn.close()
                    

    def get_module_quizzes(self, module_id):
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                SELECT * FROM quizzes 
                WHERE module_id = %s 
                ORDER BY quiz_number
                """, (module_id,))
                return cursor.fetchall()
        finally:
            conn.close()

    def get_random_questions_for_module(self, module_id, count=5):
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                SELECT q.* FROM quiz_questions q
                JOIN quizzes z ON q.quiz_id = z.id
                WHERE z.module_id = %s
                ORDER BY RAND()
                LIMIT %s
                """, (module_id, count))
                return cursor.fetchall()
        finally:
            conn.close()

    def get_user_by_username(self, username):
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
                return cursor.fetchone()
        finally:
            conn.close()

    def get_user_progress(self, user_id):
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                SELECT m.name as module_name, up.completed 
                FROM user_progress up
                JOIN modules m ON up.module_id = m.id
                WHERE up.user_id = %s
                """, (user_id,))
                
                progress = {}
                completed_modules = []
                
                for row in cursor.fetchall():
                    progress[row['module_name']] = row['completed']
                    if row['completed']:
                        completed_modules.append(row['module_name'])
                
                return {'progress': progress, 'completed_modules': completed_modules}
        finally:
            conn.close()

    def get_all_modules(self):
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                # Get all modules
                cursor.execute("SELECT id, name, title FROM modules")
                modules_data = {row['name']: {'title': row['title'], 'id': row['id'], 'lessons': []} for row in cursor.fetchall()}
                
                # Get all lessons
                cursor.execute("""
                SELECT l.*, m.name as module_name 
                FROM lessons l
                JOIN modules m ON l.module_id = m.id
                ORDER BY l.module_id, l.lesson_number
                """)
                
                for lesson in cursor.fetchall():
                    module_name = lesson['module_name']
                    modules_data[module_name]['lessons'].append({
                        'id': lesson['lesson_number'],
                        'title': lesson['title'],
                        'content': lesson['content']
                    })
                
                return modules_data
        finally:
            conn.close()

    def save_final_test(self, user_id, test_id, questions):
        """Save a generated final test in the database"""
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                # Create test entry
                cursor.execute("""
                INSERT INTO final_tests 
                (user_id, test_id, total_questions) 
                VALUES (%s, %s, %s)
                """, (user_id, test_id, len(questions)))
                
                # Save references to the questions
                for question in questions:
                    cursor.execute("""
                    INSERT INTO final_test_questions 
                    (test_id, question_id) 
                    VALUES (%s, %s)
                    """, (test_id, question['id']))
                
                conn.commit()
                return True
        except Exception as e:
            print(f"Error saving final test: {e}")
            return False
        finally:
            conn.close()

    def get_final_test_questions(self, test_id):
        """Get all questions for a final test"""
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                SELECT q.*, ftq.id as test_question_id, m.name as module_name
                FROM final_test_questions ftq
                JOIN quiz_questions q ON ftq.question_id = q.id
                JOIN quizzes qz ON q.quiz_id = qz.id
                JOIN modules m ON qz.module_id = m.id
                WHERE ftq.test_id = %s
                """, (test_id,))
                
                return cursor.fetchall()
        finally:
            conn.close()

    def save_test_answer(self, test_id, question_id, user_answer, correct):
        """Save a user's answer to a test question"""
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                UPDATE final_test_questions
                SET user_answer = %s, correct = %s
                WHERE test_id = %s AND question_id = %s
                """, (user_answer, correct, test_id, question_id))
                
                conn.commit()
                return True
        except Exception as e:
            print(f"Error saving test answer: {e}")
            return False
        finally:
            conn.close()

    def save_final_test_results(self, user_id, test_id, score, total, passed):
        """Save the final results of a test"""
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                UPDATE final_tests
                SET score = %s, total_questions = %s, passed = %s, completion_date = CURRENT_TIMESTAMP
                WHERE user_id = %s AND test_id = %s
                """, (score, total, passed, user_id, test_id))
                
                conn.commit()
                return True
        except Exception as e:
            print(f"Error saving test results: {e}")
            return False
        finally:
            conn.close()

    def get_user_test_history(self, user_id):
        """Get history of all tests taken by a user"""
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                SELECT * FROM final_tests
                WHERE user_id = %s
                ORDER BY completion_date DESC
                """, (user_id,))
                
                return cursor.fetchall()
        finally:
            conn.close()

    def create_guest_user(self):
        guest_username = 'guest_' + ''.join(random.choices(string.digits, k=6))
        guest_password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
        
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO users (username, password, is_guest) VALUES (%s, %s, TRUE)",
                    (guest_username, generate_password_hash(guest_password))
                )
                conn.commit()
                return guest_username
        finally:
            conn.close()

    def upgrade_guest_account(self, guest_username, new_username, password, email):
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                # Get current guest user
                cursor.execute("SELECT id FROM users WHERE username = %s", (guest_username,))
                guest_user = cursor.fetchone()
                
                if guest_user:
                    # Create new user account
                    cursor.execute(
                        "INSERT INTO users (username, password, email, is_guest) VALUES (%s, %s, %s, FALSE)",
                        (new_username, generate_password_hash(password), email)
                    )
                    new_user_id = cursor.lastrowid
                    
                    # Transfer progress from guest account to new account
                    cursor.execute("""
                    INSERT INTO user_progress (user_id, module_id, completed, completion_date)
                    SELECT %s, module_id, completed, completion_date
                    FROM user_progress
                    WHERE user_id = %s
                    """, (new_user_id, guest_user['id']))
                    
                    # Transfer certificates if any
                    cursor.execute("""
                    INSERT INTO certificates (user_id, module_id, score, total_questions, filename, created_at)
                    SELECT %s, module_id, score, total_questions, filename, created_at
                    FROM certificates
                    WHERE user_id = %s
                    """, (new_user_id, guest_user['id']))
                    
                    # Delete guest user
                    cursor.execute("DELETE FROM users WHERE id = %s", (guest_user['id'],))
                    
                    conn.commit()
                    return new_user_id
        finally:
            conn.close()
        return None

    def register_user(self, username, password, email, phone):
        from main import save_user_to_json
        print(f"Registering user: {username} with email: {email}")
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO users (username, password, email, phone, is_guest) VALUES (%s, %s, %s, %s, FALSE)",
                    (username, generate_password_hash(password), email, phone)
                )
                # Get the last inserted ID
                user_id = cursor.lastrowid
                conn.commit()
                
                # Also save to JSON file
                save_user_to_json(user_id, username, email, password, phone)
                
                return user_id
        finally:
            conn.close()


    def save_contact_form(self, name, email, subject, message, newsletter):
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                # Check if contacts table exists, if not create it
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS contacts (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    email VARCHAR(100) NOT NULL,
                    subject VARCHAR(200) NOT NULL,
                    message TEXT NOT NULL,
                    newsletter BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """)
                
                cursor.execute(
                    "INSERT INTO contacts (name, email, subject, message, newsletter) VALUES (%s, %s, %s, %s, %s)",
                    (name, email, subject, message, newsletter)
                )
                
                # If newsletter subscription was checked
                if newsletter:
                    # Check if newsletters table exists, if not create it
                    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS newsletter_subscribers (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        email VARCHAR(100) UNIQUE NOT NULL,
                        name VARCHAR(100),
                        subscribed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                    """)
                    
                    # Add to newsletter subscribers (ignoring duplicates)
                    cursor.execute(
                        "INSERT IGNORE INTO newsletter_subscribers (email, name) VALUES (%s, %s)",
                        (email, name)
                    )
                
                conn.commit()
                return True
        except Exception as e:
            return False
        finally:
            conn.close()

    def get_module_data(self, module_name):
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM modules WHERE name = %s", (module_name,))
                return cursor.fetchone()
        finally:
            conn.close()

    def get_lessons_for_module(self, module_id):
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                SELECT * FROM lessons 
                WHERE module_id = %s 
                ORDER BY lesson_number
                """, (module_id,))
                return cursor.fetchall()
        finally:
            conn.close()

    def get_lesson_data(self, module_id, lesson_id):
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                SELECT * FROM lessons 
                WHERE module_id = %s AND lesson_number = %s
                """, (module_id, lesson_id))
                return cursor.fetchone()
        finally:
            conn.close()

    def update_user_progress(self, user_id, module_id):
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                # Check if there's already a progress record
                cursor.execute("""
                SELECT * FROM user_progress 
                WHERE user_id = %s AND module_id = %s
                """, (user_id, module_id))
                
                if not cursor.fetchone():
                    # Create new progress record
                    cursor.execute("""
                    INSERT INTO user_progress (user_id, module_id, completed)
                    VALUES (%s, %s, FALSE)
                    """, (user_id, module_id))
                    conn.commit()
        finally:
            conn.close()

    def get_quiz_data(self, module_id, quiz_id):
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                SELECT * FROM quizzes 
                WHERE module_id = %s AND id = %s
                """, (module_id, quiz_id))
                return cursor.fetchone()
        finally:
            conn.close()

    def get_quiz_questions(self, quiz_id):
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                SELECT * FROM quiz_questions 
                WHERE quiz_id = %s 
                ORDER BY question_number
                """, (quiz_id,))
                return cursor.fetchall()
        finally:
            conn.close()

    def update_quiz_tables(self):
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                # Create quizzes table if it doesn't exist
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS quizzes (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    module_id INT NOT NULL,
                    quiz_number INT NOT NULL,
                    title VARCHAR(100) NOT NULL,
                    description TEXT,
                    passing_score INT DEFAULT 70,
                    FOREIGN KEY (module_id) REFERENCES modules(id) ON DELETE CASCADE,
                    UNIQUE KEY module_quiz_num (module_id, quiz_number)
                )
                """)
                
                # Create quiz questions table if it doesn't exist
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS quiz_questions (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    quiz_id INT NOT NULL,
                    question_number INT NOT NULL,
                    question TEXT NOT NULL,
                    options JSON NOT NULL,
                    answer VARCHAR(255) NOT NULL,
                    explanation TEXT,
                    FOREIGN KEY (quiz_id) REFERENCES quizzes(id) ON DELETE CASCADE,
                    UNIQUE KEY quiz_question_num (quiz_id, question_number)
                )
                """)
                
                # Create final tests table
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS final_tests (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    test_id VARCHAR(50) NOT NULL,
                    score INT,
                    total_questions INT,
                    passed BOOLEAN,
                    completion_date TIMESTAMP NULL,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
                """)
                
                # Create table for final test questions
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS final_test_questions (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    test_id VARCHAR(50) NOT NULL,
                    question_id INT NOT NULL,
                    user_answer VARCHAR(255),
                    correct BOOLEAN,
                    INDEX (test_id)
                )
                """)
                
                conn.commit()
        finally:
            conn.close()

    def save_quiz_results(self, user_id, module_id, score, total_questions, filename):
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                # Mark module as completed
                cursor.execute("""
                UPDATE user_progress
                SET completed = TRUE, completion_date = CURRENT_TIMESTAMP
                WHERE user_id = %s AND module_id = %s
                """, (user_id, module_id))
                
                # Generate certificate
                cursor.execute("""
                INSERT INTO certificates (user_id, module_id, score, total_questions, filename)
                VALUES (%s, %s, %s, %s, %s)
                """, (user_id, module_id, score, total_questions, filename))
                
                conn.commit()
                return True
        except Exception as e:
            return False
        finally:
            conn.close()

    def get_resource_detail(self, resource_id):
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM resources WHERE resource_id = %s", (resource_id,))
                return cursor.fetchone()
        finally:
            conn.close()

    def get_all_resources(self):
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS resources (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    resource_id VARCHAR(50) UNIQUE NOT NULL,
                    title VARCHAR(100) NOT NULL,
                    description TEXT NOT NULL,
                    image VARCHAR(100),
                    content TEXT NOT NULL,
                    category VARCHAR(100),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """)
                
                cursor.execute("SELECT COUNT(*) as count FROM resources")
                count = cursor.fetchone()['count']
                
                if count == 0:
                    resources_data = [
                        ('news-in-levels', 'News in Levels', 'Read and listen to current news articles adapted for different English proficiency levels.', 
                         'news-in-levels.jpg', '...content...', 'reading listening current-events'),
                        ('essay-writing-guide', 'Essay Writing Guide', 'A comprehensive guide to writing essays, including structure, argumentation, and style tips.',
                         'essay-writing.jpg', '...content...', 'writing academic'),
                    ]
                    
                    cursor.executemany(
                        "INSERT INTO resources (resource_id, title, description, image, content, category) VALUES (%s, %s, %s, %s, %s, %s)",
                        resources_data
                    )
                    conn.commit()
                
                cursor.execute("SELECT resource_id, title, description, image, category FROM resources")
                return cursor.fetchall()
        finally:
            conn.close()