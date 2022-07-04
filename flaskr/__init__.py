import os
import sys
from select import select
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
    return response
  
  '''
  Creates an endpoint to handle GET requests 
  for all available categories.
  '''
  @cross_origin
  @app.route('/getpassList', methods=['POST'])
  def confirm_user():
    try:
      request_data =request.get_json()
      email = request_data.get('email',None)
      user  = User.query.filter(User.email == email).one_or_none()
      if user is None:        
        abort(404)
      else :
        return jsonify({
          "success":True,
          "password":user.format()['password']
        })      
    except KeyError:
      abort(404)
      
  @cross_origin
  @app.route('/postUserDetails', methods=['POST'])
  def create_user():
    try:
      request_data = request.get_json()
      fullname = request_data.get('fullname',None)      
      email = request_data.get('email',None)
      password = request_data.get('password',None)
      if fullname and email and password:
        user = User(
          fullname = fullname,          
          email = email,
          password = password
        )
        user.insert()
        return jsonify({
          "delivered":True
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

    