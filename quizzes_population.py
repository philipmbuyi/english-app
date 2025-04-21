from database import Database
import pymysql
from quiz_data import get_quiz_data

def populate_quizzes():
    """
    Populate the database with quiz data for each module.
    Will recreate tables if missing and populate missing data.
    """
    print("Checking and populating quiz data...")
    db = Database()
    
    # Force update of quiz tables to ensure they exist
    db.update_quiz_tables()
    
    # Get all module IDs
    conn = db.get_connection()
    try:
        with conn.cursor() as cursor:
            # First check if quiz_questions table exists
            cursor.execute("""
            SELECT COUNT(*) as count 
            FROM information_schema.tables 
            WHERE table_schema = DATABASE() 
            AND table_name = 'quiz_questions'
            """)
            
            quiz_questions_exists = cursor.fetchone()['count'] > 0
            
            if not quiz_questions_exists:
                # Create quiz_questions table if it doesn't exist
                print("Recreating quiz_questions table...")
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS quiz_questions (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    quiz_id INT NOT NULL,
                    question_number INT NOT NULL,
                    question TEXT NOT NULL,
                    options TEXT NOT NULL,
                    answer TEXT NOT NULL,
                    explanation TEXT,
                    UNIQUE KEY unique_quiz_question (quiz_id, question_number),
                    FOREIGN KEY (quiz_id) REFERENCES quizzes(id) ON DELETE CASCADE
                )
                """)
                conn.commit()
            
            # Get all existing quizzes and their questions for comparison
            existing_quizzes = {}
            
            cursor.execute("SELECT id, module_id, quiz_number FROM quizzes")
            for row in cursor.fetchall():
                quiz_key = f"{row['module_id']}_{row['quiz_number']}"
                existing_quizzes[quiz_key] = row['id']
            
            # Get all modules
            cursor.execute("SELECT id, name FROM modules")
            modules = {row['name']: row['id'] for row in cursor.fetchall()}

            # Get quiz data from the imported module
            quizzes_data = get_quiz_data(modules)
            
            # Process each quiz, check if it exists and has questions
            for quiz_data in quizzes_data:
                quiz_key = f"{quiz_data['module_id']}_{quiz_data['quiz_number']}"
                
                if quiz_key in existing_quizzes:
                    quiz_id = existing_quizzes[quiz_key]
                    
                    # Check if this quiz has questions
                    cursor.execute("SELECT COUNT(*) as count FROM quiz_questions WHERE quiz_id = %s", (quiz_id,))
                    question_count = cursor.fetchone()['count']
                    
                    if question_count == 0:
                        print(f"Quiz {quiz_id} exists but has no questions. Adding questions...")
                        # Add questions to existing quiz
                        for i, question in enumerate(quiz_data['questions'], 1):
                            try:
                                cursor.execute("""
                                INSERT INTO quiz_questions 
                                (quiz_id, question_number, question, options, answer, explanation)
                                VALUES (%s, %s, %s, %s, %s, %s)
                                """, (
                                    quiz_id,
                                    i,
                                    question['question'],
                                    question['options'],
                                    question['answer'],
                                    question['explanation']
                                ))
                            except pymysql.err.IntegrityError as e:
                                if e.args[0] == 1062:  # Duplicate entry error
                                    print(f"Question {i} already exists for quiz {quiz_id} - skipping")
                                    conn.rollback()  # Rollback the failed insert
                                    continue
                                else:
                                    raise  # Re-raise other integrity errors
                else:
                    # Create new quiz and questions
                    print(f"Creating new quiz for module {quiz_data['module_id']}, number {quiz_data['quiz_number']}...")
                    try:
                        # Insert quiz
                        cursor.execute("""
                        INSERT INTO quizzes (module_id, quiz_number, title, description)
                        VALUES (%s, %s, %s, %s)
                        """, (
                            quiz_data['module_id'],
                            quiz_data['quiz_number'],
                            quiz_data['title'],
                            quiz_data['description']
                        ))
                        
                        quiz_id = cursor.lastrowid
                        
                        # Insert questions
                        for i, question in enumerate(quiz_data['questions'], 1):
                            cursor.execute("""
                            INSERT INTO quiz_questions 
                            (quiz_id, question_number, question, options, answer, explanation)
                            VALUES (%s, %s, %s, %s, %s, %s)
                            """, (
                                quiz_id,
                                i,
                                question['question'],
                                question['options'],
                                question['answer'],
                                question['explanation']
                            ))
                        
                    except pymysql.err.IntegrityError as e:
                        if e.args[0] == 1062:  # Duplicate entry error
                            print(f"Quiz already exists for module {quiz_data['module_id']} number {quiz_data['quiz_number']} - skipping")
                            conn.rollback()  # Rollback the failed insert
                            continue
                        else:
                            raise  # Re-raise other integrity errors
            
            conn.commit()
            print("Quiz data successfully checked and populated.")
    
    except Exception as e:
        print(f"Error checking and populating quizzes: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    populate_quizzes()