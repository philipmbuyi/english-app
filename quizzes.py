import random
import json
from database import Database

class QuizManager:
    def __init__(self, db):
        self.db = db

    def get_quiz_for_module(self, module_id, quiz_id):
        """Get quiz data with questions for a specific module and quiz"""
        try:
            # No need to get module_id since we already have it
            print(f"Fetching quiz for module_id={module_id}, quiz_id={quiz_id}")
            quiz = self.db.get_quiz_data(module_id, quiz_id)
            print(f"Quiz found: {quiz}") 
            if not quiz:
                return None
            
            # Get questions for this quiz
            questions = self.db.get_quiz_questions(quiz['id'])
            
            # Format and return
            return {
                'id': quiz['id'],
                'title': quiz['title'],
                'description': quiz.get('description', ''),
                'questions': questions
            }
        except Exception as e:
            print(f"Error getting quiz: {e}")
            return None
    def get_all_module_quizzes(self, module_id):
        """Get all quizzes available for a module"""
        return self.db.get_module_quizzes(module_id)

    def grade_quiz(self, user_id, module_id, quiz_id, form_data):
        """
        Grade a quiz submission and return results
        """
        quiz_data = self.db.get_quiz_data(module_id, quiz_id)
        if not quiz_data:
            return {'error': 'Quiz not found'}
            
        questions = self.db.get_quiz_questions(quiz_data['id'])
        total_questions = len(questions)
        score = 0
        feedback = {}

        for question in questions:
            q_id = question['id']
            correct_answer = question['answer']
            user_answer = form_data.get(f'question_{q_id}')

            if user_answer == correct_answer:
                score += 1
                feedback[q_id] = {'correct': True, 'explanation': question.get('explanation', '')}
            else:
                feedback[q_id] = {
                    'correct': False,
                    'your_answer': user_answer,
                    'correct_answer': correct_answer,
                    'explanation': question.get('explanation', '')
                }

        percentage = (score / total_questions) * 100 if total_questions > 0 else 0
        passed = percentage >= quiz_data.get('passing_score', 70)  # Default 70% passing

        results = {
            'score': score,
            'total': total_questions,
            'percentage': percentage,
            'passed': passed,
            'feedback': feedback
        }

        return results

    def generate_final_test(self, user_id):
        """
        Generate a comprehensive final test covering all modules
        """
        modules = self.db.get_all_modules()
        questions = []
        modules_covered = []
        
        for module_name, module_data in modules.items():
            # Get 2-3 random questions from each module
            module_questions = self.db.get_random_questions_for_module(module_data['id'], 3)
            if module_questions:
                questions.extend(module_questions)
                modules_covered.append(module_name)
        
        # Shuffle questions for randomization
        random.shuffle(questions)
        
        # Limit to 20 questions total
        questions = questions[:20]
        
        # Create a unique test ID
        test_id = f"final_test_{user_id}_{random.randint(1000, 9999)}"
        
        # Store test questions in database
        self.db.save_final_test(user_id, test_id, questions)
        
        # Format questions for display
        formatted_questions = []
        for i, q in enumerate(questions):
            formatted_questions.append({
                'id': q['id'],
                'question': q['question'],
                'options': json.loads(q['options']),
                'question_number': i + 1
            })
        
        return {
            'test_id': test_id,
            'questions': formatted_questions,
            'modules_covered': modules_covered
        }

    def grade_final_test(self, user_id, test_id, form_data):
        """
        Grade the final test and return comprehensive results
        """
        test_questions = self.db.get_final_test_questions(test_id)
        if not test_questions:
            return {'error': 'Test not found'}
            
        total_questions = len(test_questions)
        score = 0
        feedback = {}
        module_scores = {}

        for question in test_questions:
            q_id = question['id']
            correct_answer = question['answer']
            user_answer = form_data.get(f'question_{q_id}')
            
            # Check if correct
            is_correct = (user_answer == correct_answer)
            if is_correct:
                score += 1
            
            # Save answer to database
            self.db.save_test_answer(test_id, q_id, user_answer, is_correct)
            
            # Prepare feedback
            feedback[q_id] = {
                'correct': is_correct,
                'your_answer': user_answer,
                'correct_answer': correct_answer,
                'explanation': question.get('explanation', ''),
                'module': question.get('module_name', 'Unknown')
            }
            
            # Track per-module performance
            module = question.get('module_name', 'Unknown')
            if module not in module_scores:
                module_scores[module] = {'correct': 0, 'total': 0}
            module_scores[module]['total'] += 1
            if is_correct:
                module_scores[module]['correct'] += 1

        # Calculate overall percentage
        percentage = (score / total_questions) * 100 if total_questions > 0 else 0
        passed = percentage >= 70  # Assume 70% passing
        
        # Calculate module percentages
        for module in module_scores:
            module_scores[module]['percentage'] = (
                module_scores[module]['correct'] / module_scores[module]['total'] * 100
                if module_scores[module]['total'] > 0 else 0
            )
        
        # Save overall results
        self.db.save_final_test_results(user_id, test_id, score, total_questions, passed)
        
        return {
            'score': score,
            'total': total_questions,
            'percentage': percentage,
            'passed': passed,
            'feedback': feedback,
            'module_scores': module_scores
        }