import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import sys

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
  page = request.args.get('page', 1, type=int)
  start = (page-1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  formatted_questions = [question.format() for question in selection]
  return formatted_questions[start:end] 


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  

  CORS(app, resources={r"/*": {"origins": '*'}})



  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, DELETE, OPTIONS')

    return response


  
  @app.route('/categories', methods=['GET'])
  def get_all_categories():
    selection = Category.query.order_by(Category.id).all()
    categories = {category.id: category.format() for category in selection}
    
    return jsonify({
      "success": True,
      "categories": categories
    })


  @app.route('/questions', methods=['GET'])
  def get_all_questions():
    selection_categories = Category.query.order_by(Category.id).all()
    categories = {category.id: category.format() for category in selection_categories}

    selection_questions = Question.query.order_by(Question.id).all()
    total_questions = len(selection_questions)

    questions = paginate_questions(request, selection_questions) 

    if(len(questions) == 0):
      abort(404)

    return jsonify({
      "success": True,
      "questions": questions,
      "total_questions": total_questions,
      "categories": categories
    })



  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    question = Question.query.filter(Question.id == question_id).one_or_none()
    print(question)

    if question is None:
        abort(404)

    try: 
      question.delete()
      total_questions = len(Question.query.order_by(Question.id).all())

      return jsonify({
        "success": True,
        "deleted": question_id,
        "total_questions": total_questions
      })

    except:
      abort(422)



  def search_questions(request, search_term):
    selection = Question.query.order_by(Question.id).filter(Question.question.ilike('%' + search_term + '%'))
    questions = paginate_questions(request, selection)

    return questions


  @app.route('/questions', methods=['POST'])
  def create_or_search_questions():
    body = request.get_json()

    question_text = body.get('question', None)
    answer_text = body.get('answer', None)
    difficulty = body.get('difficulty', None)
    category = body.get('category', None)
    search_term = body.get('searchTerm', None)

    try:
      if search_term:
        questions = search_questions(request, search_term)
        
        return jsonify({
          "success": True,
          "questions": questions,
          "total_questions": len(questions)
        })
            
      else:
        current_category = Category.query.filter(Category.id == category).one_or_none()

        if(current_category == None):
          abort(422)
        
        question = Question(
          question = question_text,
          answer = answer_text,
          difficulty = difficulty,
          category = current_category.id)

        question.insert()

        selection = Question.query.order_by(Question.id).all()
        questions = paginate_questions(request, selection)

        return jsonify({
          "success": True,
          "created": question.id,
          "questions": questions,
          "total_questions": len(questions)          
        })

    except:
      abort(422)


  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def get_all_questions_by_category(category_id):
    body = request.get_json()

    categories = Category.query.filter(Category.id == category_id).all()

    if not categories:
      abort(404)

    selection = Question.query.filter(Question.category == category_id).order_by(Question.id).all()

    questions = paginate_questions(request, selection) 

    if(len(questions) == 0):
      abort(404)

    return jsonify({
      'success': True,
      'current_category': category_id,
      'questions': questions,
      'total_questions': len(questions)      
    })


  @app.route('/quizz', methods=['POST'])
  def quizz():
    body = request.get_json()

    previous_questions = body.get('previous_questions', None)
    category = body.get('quiz_category', None)

    if category is None:
      abort(404)
    
    if category == 0:
      questions = Question.query.order_by(Question.id).all().filter(Question.id.notin_(previous_questions)).all()
      
    
    else:
      questions = Question.query.filter(Question.category == category).filter(Question.id.notin_(previous_questions)).all()

    if(len(questions) > 0):
      question = questions[random.randrange(0, len(questions))].format()
    else:
      question = None

    return jsonify({
      'success': True,
      'question': question,
      'quiz_category': category,
    })



  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False,
      "error": 404,
      "message": "Not found"
    }), 404

  
  @app.errorhandler(422)
  def unprocesseable(error):
    print(sys.exc_info()[1])
    return jsonify({
      "success": False,
      "error": 422,
      "message": "Unprocesseable"
    }), 422
  
  return app

    