import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    if test_config is None:
        setup_db(app)
    else:
        database_path = test_config.get('SQLALCHEMY_DATABASE_URI')
        setup_db(app, database_path=database_path)
        
    cors = CORS(app, resources={r"/*": {"origins": "*"}})
        
    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    def paginate_questions(request, selection):
        page = request.args.get("page", 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        questions = [question.format() for question in selection]
        current_questions = questions[start:end]
        return current_questions
    
    @app.route('/categories', methods=['GET'])
    def get_categories():
        categories = Category.query.order_by(Category.id).all()
        if len(categories) == 0:
            abort(404)

        return jsonify(
            {
                "success": True,
                "categories": {item.id: item.type for item in categories}
            }
        )
    
    @app.route('/questions')
    def get_questions():
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)
        categories = Category.query.order_by(Category.id).all()

        if len(current_questions) == 0:
            abort(404)

        return jsonify(
            {
                "success": True,
                "questions": current_questions,
                "totalQuestions": len(selection),
                "categories": {item.id: item.type for item in categories},
                "currentCategory": 'History'
            }
        )

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()

            if question is None:
                abort(404)

            question.delete()

            return jsonify(
                {
                    "success": True,
                    "deleted": question_id
                }
            )

        except:
            abort(422)

    
    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()
        new_question = body.get('question')
        new_answer = body.get('answer')
        new_difficulty = body.get('difficulty')
        new_category = body.get('category')
        search_term = body.get('searchTerm')

        try:
            if search_term:
                selection = Question.query.order_by(Question.id).filter(Question.question.ilike(f'%{search_term}%')).all()
                search_questions = paginate_questions(request, selection)
                category_id = selection[0].category
                current_category = Category.query.filter(Category.id == category_id).one_or_none()
                
                if search_questions == None:
                    abort(404)

                return jsonify({
                    "success": True,
                    "questions": search_questions,
                    "totalQuestions": len(Question.query.all()),
                    "currentCategory": current_category.type
                })

            else:
                question = Question(
                    question=new_question,
                    answer=new_answer,
                    category=new_category,
                    difficulty=new_difficulty
                )

                question.insert()

                questions = Question.query.all()
                current_questions = paginate_questions(request, questions)

                return jsonify({
                    'success': True,
                    'createdQuestionId': question.id,
                    'message': "Succesfully created question"
                })
        except:
            abort(422)

    
    @app.route('/categories/<int:category_id>/questions')
    def get_question_by_categories(category_id):

        try:
            selection = Question.query.filter(category_id == Question.category).all()
            current_questions = paginate_questions(request, selection)
            current_category = Category.query.filter(Category.id == category_id).one_or_none()

            return jsonify({
                    "success": True,
                    "questions": list(current_questions),
                    "totalQuestions": len(selection),
                    "currentCategory": current_category.type
                })
        except:
            abort(404)

    @app.route('/quizzes', methods=['POST'])
    def start_playing():
        try:
            body = request.get_json()
            quiz_category = body.get('quiz_category')
            previous_questions = body.get('previous_questions')
            category_id = quiz_category['id']

            if category_id == 0:
                questions = Question.query.filter(Question.id.notin_(previous_questions)).all()
            else:
                questions = Question.query.filter(Question.id.notin_(previous_questions), 
                    Question.category == category_id).all()
            
            question = None
            if(questions):
                question = random.choice(questions)

            return jsonify({
                'success': True,
                'question': question.format()
            })
        except:
            abort(422)

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"success": False, "error": 404, "message": "resource not found"}), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({"success": False, "error": 422, "message": "unprocessable"}), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400, "message": "bad request"}), 400
    
    @app.errorhandler(500)
    def bad_request(error):
        return jsonify({"success": False, "error": 500, "message": "internal server error"}), 500

    return app

