import os
from flask import Flask, request, abort, jsonify
import json
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import func
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    cors = CORS(app, resources={r"*": {"origins":"*"}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*');
        response.headers.\
            add('Access-Control-Allow-Method', 'POST, GET, PUT, DELETE');

        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    def paginate_question(page, questions):
        page = int(page)
        start_index = (page - 1) * QUESTIONS_PER_PAGE
        end_index = page * QUESTIONS_PER_PAGE

        return questions[start_index : end_index]

    def obtain_questions_list(questions):
        return [{'id':question.id, 'question': question.question,
         'answer': question.answer,'category': question.category, 
         'difficulty': question.difficulty } for question in questions]

    @app.route('/categories', methods=['GET'])
    def fetch_categories():
        try:
            all_categories = Category.query.all();
            categories = {category.id : category.type for category in all_categories}

            return jsonify({"categories": categories}), 200
        except:
            abort(404)

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions', methods=['GET'])
    def get_paginated_questions():
        page_number = request.args.get("page",1, type=int)
        all_question = Question.query.all()
        all_category = Category.query.all()

        paginated_questions = paginate_question(page_number, all_question)
        
        if len(paginated_questions) == 0:
            abort(404)

        display_questions = obtain_questions_list(paginated_questions)

        return jsonify({
            'questions': display_questions,
            'totalQuestions': len(all_question),
            'categories': {category.id : category.type for category in all_category},
            'currentCategory': None,
        }), 200

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.get(question_id)

        if question == None:
            abort(404)

        question.delete()
        return jsonify({'success': True}), 200

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/question', methods=['POST'])
    def post_question():
        body = request.get_json()

        if body['question'] == None or body['answer'] ==\
            None or body['difficulty'] == None:
            abort(422)

        try:
            question = Question(question=body['question'],
             answer=body['answer'], difficulty=body['difficulty'], 
             category=body['category'])

            question.insert()

            return jsonify({
                'success': True,
                'message': 'OK'
            }), 200

        except:
            abort(422)


    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/questions/searchedTerm', methods=['POST'])
    def fetch_question_by_search_term():
        term_searched = request.get_json()['searchTerm']
        current_category_id = request.args.get('category')
        categories = Category.query.all()


        if int(current_category_id) > len(categories):
            abort(404)

        # if category == None:
        #     abort(404)

        # if current_category == 'null':
        #     current_category = None

        # if current_category is None:
        #     questions = Question.query.filter(Question.question.\
        #         ilike(f'%{term_searched}%')).all()
        if current_category_id == 'undefined':
            questions = Question.query.filter(Question.question.\
                ilike(f'%{term_searched}%')).all()
        else:
            questions = Question.query.filter(Question.category == current_category_id).filter(Question.question.ilike(f'% {term_searched}%')).all()

        if questions == None:
            abort(404)

        questions_to_display = obtain_questions_list(questions)


        return jsonify({
            'questions': questions_to_display,
            'total_questions': len(questions),
            'current_category': current_category_id
        }), 200


    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def fetch_category_questions(category_id):
        questions = Question.query.filter(Question.category == category_id).all()
        page = request.args.get('page', 1, type=int)

        if len(questions) == 0:
            abort(404)

        paginated_questions = paginate_question(page, questions)

        questions_to_display = obtain_questions_list(paginated_questions)

        return jsonify({
            'questions': questions_to_display,
            'total_questions': len(questions),
            'current_category': category_id
        }), 200



    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes', methods=['POST'])
    def fetch_quiz():
        body = request.get_json()
        current_question = None

        try:
            category_id = body['quiz_category']['id']
            previous_questions = body['previous_questions']

            current_category = Category.query.all()

            if int(category_id) > len(current_category):
                abort(404)


            if category_id == 0:
                category_questions = Question.query.order_by(func.random()).all()
            else:
                category_questions = Question.query.filter(Question.category == category_id).order_by(func.random()).\
                    all()

            for question in category_questions:
                if question.id in previous_questions:
                    continue;
                else:
                    previous_questions.append(question.id)
                    current_question = question
                    break

            
            if current_question == None:
                abort(404)

            return jsonify({
                'question': {
                    'id': current_question.id,
                    'question': current_question.question,
                    'answer': current_question.answer,
                    'difficulty': current_question.difficulty,
                    'category': category_id
                },
                'previousQuestions': previous_questions
            }), 200
        except:
            abort(400)



    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def question_or_page_not_found(err):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Page or Question not Found'
        }), 404

    @app.errorhandler(400)
    def Bad_request(err):
        return jsonify({
            'success': False,
            'error': 400,
            'message': '😄, Request not valid'
        }), 404
    @app.errorhandler(500)
    def Internal_server_error(err):
        return jsonify({
            'success': False,
            'error': 500,
            'message': '😥, Error in Server'
        }), 500

    @app.errorhandler(422)
    def question_or_page_not_found(err):
        return jsonify({
            'success': False,
            'error': 422,
            'message': '🤔, request could not be processed'
        }), 422

    @app.errorhandler(405)
    def bad_method(err):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'Method not permitted'
        }), 405

    return app

