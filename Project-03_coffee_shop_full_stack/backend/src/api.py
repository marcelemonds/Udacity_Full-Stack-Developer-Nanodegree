import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
# db_drop_and_create_all()

'''--------------------------------------------------------------
GET /drinks
    it is a public endpoint
    it contains only the drink.short() data representation
returns status code 200 and json {"success": True, "drinks": drinks}
    where drinks is the list of drinks
    or appropriate status code indicating reason for failure
--------------------------------------------------------------'''
@app.route('/', methods=['GET'])
@app.route('/drinks', methods=['GET'])
def get_drinks():
    drinks_raw = Drink.query.all()
    drinks = [drink.short() for drink in drinks_raw]
    return jsonify({
      'success': True,
      'drinks': drinks
    }), 200


'''--------------------------------------------------------------
GET /drinks-detail
    it requires the 'get:drinks-detail' permission
    it contains the drink.long() data representation
returns status code 200 and json {"success": True, "drinks": drinks}
    where drinks is the list of drinks
    or appropriate status code indicating reason for failure
--------------------------------------------------------------'''
@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_detail(payload):
    drinks_raw = Drink.query.all()
    return jsonify({
      'success': True,
      'drinks': [drink.long() for drink in drinks_raw]
    }), 200


'''--------------------------------------------------------------
POST /drinks
    it creates a new row in the drinks table
    it requires the 'post:drinks' permission
    it contains the drink.long() data representation
returns status code 200 and json {"success": True, "drinks": drink}
    where drink an array containing only the newly created drink
    or appropriate status code indicating reason for failure
--------------------------------------------------------------'''
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def post_drinks(payload):
    body = request.get_json()
    try:
        title = body['title']
        recipe = json.dumps(body['recipe'])
        drink = Drink(
            title=title,
            recipe=recipe
        )
        drink.insert() 
        return jsonify({
            'success': True,
            'drinks': drink.long()
        }), 200
    except Exception as e:
        print(e)
        abort(422)


'''--------------------------------------------------------------
PATCH /drinks/<id>
    where <id> is the existing model id
    it responds with a 404 error if <id> is not found
    it updates the corresponding row for <id>
    it requires the 'patch:drinks' permission
    it contains the drink.long() data representation
returns status code 200 and json {"success": True, "drinks": drink}
    where drink an array containing only the updated drink
    or appropriate status code indicating reason for failure
--------------------------------------------------------------'''
@app.route('/drinks/<id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def patch_drinks(payload, id):
    try:
        drink = Drink.query.get(id)
        if not drink:
            abort(404)
        body = request.get_json()
        for part in body.keys():
            if part == 'title':
                drink.title = body['title']
            elif part == 'recipe':
                drink.recipe = json.dumps(body['recipe'])
        drink.update()
        return jsonify({
            'success': True,
            'drinks': [drink.long()]
        }), 200
    except Exception as e:
        print(e)
        abort(422)   


'''--------------------------------------------------------------
DELETE /drinks/<id>
    where <id> is the existing model id
    it responds with a 404 error if <id> is not found
    it deletes the corresponding row for <id>
    it requires the 'delete:drinks' permission
returns status code 200 and json {"success": True, "delete": id}
    where id is the id of the deleted record
    or appropriate status code indicating reason for failure
--------------------------------------------------------------'''
@app.route('/drinks/<id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drinks(payload, id):
    try:
        drink = Drink.query.get(id)
        if not drink:
            abort(404)
        drink.delete()
        return jsonify({
            'success': True,
            'delete': id
        }), 200
    except Exception as e:
        print(e)
        abort(422)


'''--------------------------------------------------------------
Error Handling
--------------------------------------------------------------'''
@app.errorhandler(400)
def bad_request(e):
    return jsonify({
      'success': False,
      'error': 400,
      'message': 'Bad Request'
    }), 400


@app.errorhandler(404)
def not_found(e):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'Not Found'
    }), 404


@app.errorhandler(422)
def unprocessable_entity(e):
    return jsonify({
        'success': False,
        'error': 422,
        'message': 'Unprocessable Entity'
    }), 422


@app.errorhandler(500)
def internal_server_error(e):
    return jsonify({
        'success': False,
        'error': 500,
        'message': 'Internal Server Error'
    }), 500


@app.errorhandler(AuthError)
def autherror(error):
    return jsonify({
        'success': False,
        'error': error.status_code,
        'message': error.error['description']
    }), error.status_code
