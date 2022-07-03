import os
import sys
from select import select
from tkinter.messagebox import QUESTION
from unicodedata import category
from xmlrpc.client import FastMarshaller
from flask import (
  Flask, 
  request, 
  abort, 
  jsonify
  )
from flask_sqlalchemy import SQLAlchemy #, _or
from flask_cors import *
from random import randint

from models import setup_db, User

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)
  
  # CORS Headers

  '''
    Using the after_request decorator to set Access-Control-Allow
  '''
  
  @app.after_request
  def after_request(response):
    response.headers.add(
      'Access-Control-Allow-Headers', 'Content-Type,Authorization'
      )
    response.headers.add(
      'Access-Control-Allow-Methods', 'GET,POST,PATCH,DELETE,OPTIONS'
      )
    response.headers.add(
      'Access-Control-Allow-Credentials', 'true'
      )                  
    return response
  
  def paginated_questions(request,response):
    page = request.args.get("page", 1, type=int)       
    start= (page-1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = [question.format() for question in response]
    selected_questions = questions[start:end]
    return selected_questions
    
  
  
  '''
  Creates an endpoint to handle GET requests 
  for all available categories.
  '''
  @cross_origin
  @app.route('/create/signup', methods=['POST'])
  def create_user():
    try:
      request_data = request.get_json()
      firstname = request_data.get('firstname',None)
      lastname = request_data.get('lastname',None)
      email = request_data.get('email',None)
      password = request_data.get('password',None)
      if firstname and lastname and email and password:
        user = User(
          firstname = firstname,
          lastname = lastname,
          email = email,
          password = password
        )
        user.insert()
        return jsonify({
          "success":True
        })
      else:
        abort(422)
    except KeyError:
      abort(404)
    
    
    
    

  '''
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      'success':False,
      'error':404,
      'message':'resource not found'
    }),404
  
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      'success': False,
      'error': 400,
      'message': 'bad request'
    }),400
  
  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      'success': False,
      'error': 422,
      'message': 'unprocessable'      
    }),422
  
  @app.errorhandler(405)
  def not_allowed(error):
    return jsonify({
      'success': False,
      'error': 405,
      'message': 'method not allowed'
    }),405
  return app

    