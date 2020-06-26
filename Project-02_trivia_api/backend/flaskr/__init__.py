import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import json
from models import db, setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''-------------------------------------------------------------------------------------
  Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  -------------------------------------------------------------------------------------'''
  cors = CORS(app, resources={r"/*": {"origins": "*"}})

  '''-------------------------------------------------------------------------------------
  after_request decorator to set Access-Control-Allow
  -------------------------------------------------------------------------------------'''
  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
      response.headers.add('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')
      return response

  '''-------------------------------------------------------------------------------------
  endpoint to handle GET requests for all available categories
  -------------------------------------------------------------------------------------'''
  @app.route('/categories', methods=['GET'])
  def categories_get():
    categories = Category.query.all()
    return jsonify({
      'success': True,
      'categories': [category.format() for category in categories]
    }), 200

  '''-------------------------------------------------------------------------------------
  endpoint to handle GET requests for questions, including pagination (every 10 questions)
  -------------------------------------------------------------------------------------'''
  @app.route('/', methods=['GET'])
  @app.route('/questions', methods=['GET'])
  def questions_get():
    page = request.args.get('page', 1, type=int)
    max_questions = request.args.get('max', QUESTIONS_PER_PAGE, type=int)
    start = (page - 1) * max_questions
    
    questions = Question.query.offset(start).limit(max_questions).all()
    categories = Category.query.all()
    total_questions = Question.query.count()
    if not questions:
      abort(404)
    
    return jsonify({
      'success': True,
      'questions': [question.format() for question in questions],
      'categories': [category.format() for category in categories],
      'total_questions': total_questions,
      'current_category': 'all'
    }), 200

  '''-------------------------------------------------------------------------------------
  endpoint to DELETE question using a question ID
  -------------------------------------------------------------------------------------'''
  @app.route('/questions/<int:id>', methods=['DELETE'])
  def question_delete(id):
    try:
      question = Question.query.get(id)
      if question is None:
        abort(404)
      question.delete()
      return jsonify({
        'success': True,
        'message': f'Successfully deleted question #{id}'
      })
    except Exception as e:
      db.session.rollback()
      raise e
    finally:
      db.session.close()

  '''-------------------------------------------------------------------------------------
  endpoint to POST a new question or to get questions based on a search term
  -------------------------------------------------------------------------------------'''
  @app.route('/questions', methods=['POST'])
  def questions_post():
    try:
      data = json.loads(request.data)
      if 'searchTerm' in data.keys():
        search = f'%{data["searchTerm"].lower()}%'
        questions = Question.query.filter(db.func.lower(Question.question).like(search)).all()
        if not questions:
          abort(404)
        return jsonify({
                'success': True,
                'questions': [question.format() for question in questions],
                'total_questions': len(questions),
                'current_category': None
              }), 200
      validation = ['question', 'answer', 'difficulty', 'category']
      for key in validation:
        if key not in data.keys() or data[key] is '':
          abort(400)
      new_question = Question(**data)
      new_question.insert()
      return jsonify({
        'success': True,
        'data': new_question.format()
      }), 201
    except Exception as e:
      db.session.rollback()
      raise e
    finally:
      db.session.close()

  '''-------------------------------------------------------------------------------------
  GET endpoint to get questions based on category
  -------------------------------------------------------------------------------------'''
  @app.route('/categories/<int:id>/questions', methods=['GET'])
  def questions_get_by_category(id):
    page = request.args.get('page', 1, type=int)
    max_questions = request.args.get('max', QUESTIONS_PER_PAGE, type=int)
    start = (page - 1) * max_questions

    questions = Question.query.filter_by(category=int(id)).offset(start).limit(max_questions).all()
    category = Category.query.get(id)
    total_questions = Question.query.filter_by(category=int(id)).count()

    if not questions:
      abort(404)

    return jsonify({
      'success': True,
      'questions': [question.format() for question in questions],
      'total_questions': total_questions,
      'current_category': category.format()
    }), 200

  '''-------------------------------------------------------------------------------------
  POST endpoint to get questions to play the quiz
  -------------------------------------------------------------------------------------'''
  @app.route('/quizzes', methods=['POST'])
  def questions_get_for_quiz():
    try:
      data = json.loads(request.data)
      validation = ['previous_questions', 'quiz_category']
      for key in validation:
        if key not in data.keys():
          abort(400)
      result = db.session.query(Question).filter(Question.id.notin_(data['previous_questions'])).all()
      questions_unfiltered = [question.format() for question in result]
      questions_filtered = [question for question in questions_unfiltered if question['category'] == data['quiz_category']['id']]
      if not questions_filtered:
        abort(404)
      question = random.choice(questions_filtered)

      return jsonify({
        'success': True,
        'question': question
      }), 200
    except Exception as e:
      db.session.rollback()
      raise e
    finally:
      db.session.close()

  '''-------------------------------------------------------------------------------------
  error handlers for all expected errors
  -------------------------------------------------------------------------------------'''
  @app.errorhandler(400)
  def bad_request(e):
    return jsonify({
      'success': False,
      'error': 400,
      'message': 'Bad Request'
    })

  @app.errorhandler(404)
  def not_found(e):
    return jsonify({
      'success': False,
      'error': 404,
      'message': 'Not Found'
    })

  @app.errorhandler(422)
  def unprocessable_entity(e):
    return jsonify({
      'success': False,
      'error': 422,
      'message': 'Unprocessable Entity'
    })

  @app.errorhandler(500)
  def internal_server_error(e):
    return jsonify({
      'success': False,
      'error': 500,
      'message': 'Internal Server Error'
    })

  return app

    