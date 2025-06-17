from flask import Blueprint, request, jsonify, current_app, make_response

from backend.db_connection import db

users = Blueprint("users", __name__)

@users.route("/users/role/<int:userRoleID>", methods=["GET"])
def get_users(userRoleID):
    current_app.logger.info('GET /users/role/<userRoleID> route entered')
    query = '''
        SELECT userID, age, countryOfOrigin, firstName, lastName, partyID, watchListID, userRoleID
        FROM user
        WHERE userRoleID = %s;
    '''
    cursor = db.get_db().cursor()

    cursor.execute(query, (userRoleID))
    retrieved_users = cursor.fetchall()
    cursor.close()
    
    current_app.logger.info("GET /users route success")
    response = make_response(jsonify(retrieved_users))
    response.status_code = 200
    
    return response


@users.route("/users/<int:userID>", methods=["GET"])
def get_user(userID):
    current_app.logger.info("GET /user/<int:userID> route entered")

    query = '''
        SELECT userID, age, countryOfOrigin, firstName, lastName, partyID, watchListID, userRoleID
        FROM user
        WHERE userID = %s;
    '''

    cursor = db.get_db().cursor()

    cursor.execute(query, (userID))
    retrieved_users = cursor.fetchall()
    cursor.close()

    current_app.logger.info("GET /users route success")
    response = make_response(jsonify(retrieved_users))
    response.status_code = 200

    return response


@users.route("/users/<int:userID>/role", methods=["GET"])
def get_user_role(userID):
    current_app.logger.info("GET /user/<int:userID>/role route entered")

    query = '''
        SELECT userRoleName
        FROM user
        JOIN userRole ON user.userRoleID = userRole.userRoleID
        WHERE userID = %s;
    '''

    cursor = db.get_db().cursor()

    cursor.execute(query, (userID))
    retrieved_users = cursor.fetchall()
    cursor.close()

    current_app.logger.info("GET /users route success")
    response = make_response(jsonify(retrieved_users))
    response.status_code = 200

    return response


    
