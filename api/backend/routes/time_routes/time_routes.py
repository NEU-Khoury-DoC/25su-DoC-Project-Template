from flask import Blueprint, request, jsonify, current_app, make_response
from mysql.connector import Error


from backend.db_connection import db

time = Blueprint("time", __name__)

@time.route("/times", methods=['GET'])
def get_info():
    current_app.logger.info('GET /time route entered')
    query = '''
        SELECT party, percent_dissent, adjusted_week
        FROM dissentOverTimeData;
    '''
    cursor = db.get_db().cursor()

    cursor.execute(query)
    retrieved_users = cursor.fetchall()
    cursor.close()

    current_app.logger.info("GET /time route success")
    response = make_response(jsonify(retrieved_users))
    response.status_code = 200
    
    return response