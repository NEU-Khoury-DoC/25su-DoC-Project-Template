from flask import Blueprint, jsonify, current_app, make_response, request
from mysql.connector import Error

from backend.db_connection import db

parties = Blueprint("parties", __name__)

@parties.route("/parties", methods=["GET"])
def get_all_parties():
    current_app.logger.info('GET /parties route entered')
    query = '''
        SELECT partyID, partyCohesionScore, partyName
        FROM political_party
    '''
    cursor = db.get_db().cursor()

    cursor.execute(query)
    retrieved_parties = cursor.fetchall()
    cursor.close()

    current_app.logger.info("GET /parties route success")
    response = make_response(jsonify(retrieved_parties))
    response.status_code = 200
    
    return response



@parties.route("/parties/<int:partyID>", methods=['GET'])
def get_party(partyID):
    current_app.logger.info('GET /party/<int:partyID> route entered')
    query = '''
        SELECT partyID, partyCohesionScore, partyName
        FROM political_party
        WHERE partyID = %s
    '''
    cursor = db.get_db().cursor()

    cursor.execute(query, (partyID))
    retrieved_party = cursor.fetchone()
    cursor.close()

    current_app.logger.info("GET /party/<int:partyID> route success")
    response = make_response(jsonify(retrieved_party))
    response.status_code = 200
    
    return response


@parties.route("/parties/<int:partyID>/score", methods=['GET'])
def get_overall_party_loyalty(partyID):
    current_app.logger.info('GET /party/<int:partyID>/score route entered')
    query = '''
        SELECT partyCohesionScore
        FROM political_party
        WHERE partyID = %s
    '''
    cursor = db.get_db().cursor()

    cursor.execute(query, (partyID))
    retrieved_party = cursor.fetchone()
    cursor.close()

    current_app.logger.info("GET /party/<int:partyID>/score route success")
    response = make_response(jsonify(retrieved_party))
    response.status_code = 200
    
    return response

@parties.route("/parties/<int:partyID>/score", methods=['PUT'])
def update_mep_loyalty_score(partyID):
    current_app.logger.info('PUT /parties/<int:partyID>/score route entered')
    
    try:
        data = request.json()
        
        required_fields = ["partyCohesionScore"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        cursor = db.get_db().cursor()
        query = "UPDATE parties SET partyCohesionScore, %s WHERE partyID = %s"

        cursor.execute(query, (data['partyCohesionScore'], partyID))
        cursor.close()


        current_app.logger.info("PUT /parties/<int:partyID>/score route success")

        return (jsonify({"message": "Parties score successfully updated", "partyID": {partyID}, "partyCohesionScore": data['partyCohesionScore']}), 201,)

    except Error as e:
        return jsonify({"error": str(e)}), 500
