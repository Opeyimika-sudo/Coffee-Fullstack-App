import os
from turtle import update
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)


    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type, Authorization, True"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PATCH,PUT,POST,DELETE,OPTIONS"
        )
        return response
    '''
    @TODO uncomment the following line to initialize the datbase
    !! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
    !! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
    !! Running this funciton will add one
    '''
    # db_drop_and_create_all()

    # ROUTES
    '''
    @TODO implement endpoint
        GET /drinks
            it should be a public endpoint
            it should contain only the drink.short() data representation
        returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
            or appropriate status code indicating reason for failure

    '''
    @app.route('/drinks', methods=["GET"])
    def get_drinks():
        try:
            drinks = Drink.query.all()
            if len(drinks) == 0:
                abort(404)

            all_drinks = [drink.short() for drink in drinks]

            return jsonify({
                 "status": 200,
                "success": True,
                "drinks": all_drinks
            })
        
        except:
            abort(422)

    '''
    @TODO implement endpoint
        GET /drinks-detail
            it should require the 'get:drinks-detail' permission
            it should contain the drink.long() data representation
        returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
            or appropriate status code indicating reason for failure
    '''
    @app.route('/drinks-detail', methods=['GET'])
    @requires_auth('get:drinks-detail')   
    def get_drink_in_detail(payload):
        drinks = Drink.query.all()

        all_drinks = []

        for drink in drinks:
            all_drinks.append(drink.long())

        print(all_drinks)
        print(type(all_drinks))

        return jsonify({
            'status': 200,
            'success': True,
            'drinks': all_drinks
        })


    '''
    @TODO implement endpoint
        POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
        returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
    # '''
    @app.route('/drinks', methods=['POST'])
    @requires_auth('post:drinks')     
    def add_new_drink(payload):
        # print(token)
        drink = request.get_json()

        if len(drink) == 0:
            abort(404)
        
        newTitle = drink.get('title')
        newRecipe= json.dumps(drink.get('recipe'))

        try:
            if request.method== 'POST':
                newDrink= Drink(title=newTitle, recipe=newRecipe)
                newDrink.insert()
                
                return jsonify({
                    'success': True,
                    "drinks": newDrink.long()
                })

        except:
            abort(422)

    '''
    @TODO implement endpoint
        PATCH /drinks/<id>
            where <id> is the existing model id
            it should respond with a 404 error if <id> is not found
            it should update the corresponding row for <id>
            it should require the 'patch:drinks' permission
            it should contain the drink.long() data representation
        returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
            or appropriate status code indicating reason for failure
    '''
    @app.route('/drinks/<id>', methods=['PATCH'])
    @requires_auth('patch:drinks')    
    def update_drink(payload, id):
        drink = Drink.query.filter(id == Drink.id).one_or_none()

        body = request.get_json()

        if drink is None:
            abort(404)

        try:
            if 'title' in body:
                newTitle = body.get('title')
            else:
                newTitle = drink.title

            if 'recipe' in body:
                newRecipe = json.dumps(body.get('recipe'))
            else:
                newRecipe = drink.recipe
            
            drink.title = newTitle
            drink.recipe = newRecipe
            drink.update()

            return jsonify({
                "success": True,
                "drinks": drink.long()
            })

        except:
            abort(422)

    '''
    @TODO implement endpoint
        DELETE /drinks/<id>
            where <id> is the existing model id
            it should respond with a 404 error if <id> is not found
            it should delete the corresponding row for <id>
            it should require the 'delete:drinks' permission
        returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
            or appropriate status code indicating reason for failure
    '''
    @app.route('/drinks/<id>', methods=['DELETE'])
    @requires_auth('delete:drinks')
    def delete_drink(payload, id):
        drink = Drink.query.filter(id == Drink.id).one_or_none()

        if drink is None:
            abort(404)

        try:
            drink.delete()

            return jsonify({
                "success": True,
                "delete": id
            })
        
        except:
            abort(422)
        

    # Error Handling
    '''
    Example error handling for unprocessable entity
    '''


    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "not processable"
        }), 422


    '''
    @TODO implement error handlers using the @app.errorhandler(error) decorator
        each error handler should return (with approprate messages):
                jsonify({
                        "success": False,
                        "error": 404,
                        "message": "resource not found"
                        }), 404

    '''

    '''
    @TODO implement error handler for 404
        error handler should conform to general task above
    '''
    @app.errorhandler(404)
    def page_not_found(error):
        return jsonify({
            'success': False,
            'status': 404,
            'message': 'Resource not found'
        }), 404


    '''
    @TODO implement error handler for AuthError
        error handler should conform to general task above
    '''
    # @app.errorhandler(AuthError)
    # def auth_error(error):
    #     return jsonify({
    #         'success': False,
    #         'status': 401,
    #         'message': 'Authentication error'
    #     }), AuthError

   


    return app