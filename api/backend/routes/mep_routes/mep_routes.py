from flask import Blueprint, request, jsonify, current_app, make_response
from mysql.connector import Error


from backend.db_connection import db

meps = Blueprint("meps", __name__)

@meps.route("/meps", methods=['GET'])
def get_all_meps():
    current_app.logger.info('GET /meps route entered')
    query = '''
        SELECT mepID, name, countryOfOrigin, loyaltyScore, percentDisagree, percentTurnout, partyID, recommendedPartyID, photoURL
        FROM mep;
    '''
    cursor = db.get_db().cursor()

    cursor.execute(query)
    retrieved_users = cursor.fetchall()
    cursor.close()

    current_app.logger.info("GET /meps route success")
    response = make_response(jsonify(retrieved_users))
    response.status_code = 200
    
    return response

@meps.route("/meps", methods=['POST'])
def create_mep():
    current_app.logger.info('POST /meps route entered')

    try:
        data = request.json()

        required_fields = ["mepID", "name", "countryOfOrigin", "photoURL"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        cursor = db.get_db().cursor()

        query = """
            INSERT INTO meps (mepID, name, countryOfOrigin, photoURL)
            VALUES (%s, %s, %s, %s);
        """

        cursor.execute(query, (data['mepID'],
                                data['name'],
                                data['countryOfOrigin'],
                                data['photoURL']))
    
        db.get_db().commit()
        cursor.close()
        
        return (jsonify({"message": "MEP created successfully", "mepID": data["mepID"]}), 201,)
        
    except Error as e:
        return jsonify({"error": str(e)}), 500

@meps.route("/meps/<int:mepID>", methods=['GET'])
def get_mep(mepID):
    current_app.logger.info('GET /mep/<int:mepID> route entered')
    query = '''
        SELECT mepID, name, countryOfOrigin, loyaltyScore, partyID, recommendedPartyID, photoURL
        FROM mep
        WHERE mepID = %s;
    '''
    cursor = db.get_db().cursor()

    cursor.execute(query, (mepID))
    retrieved_mep = cursor.fetchone()
    cursor.close()

    current_app.logger.info("GET /mep/<int:mepID> route success")
    response = make_response(jsonify(retrieved_mep))
    response.status_code = 200
    
    return response


@meps.route("/mep/<int:mepID>/score", methods=['GET'])
def get_mep_loyalty_score(mepID):
    current_app.logger.info(f'GET /mep/{mepID}/score route entered')

    query = '''
        SELECT agreedPct, dissentedPct, notVotedPct
        FROM mep
        WHERE mepID = %s;
    '''

    try:
        cursor = db.get_db().cursor()
        cursor.execute(query, (mepID,))
        result = cursor.fetchone()
        cursor.close()

        if result:
            agreed, dissented, not_voted = result
            return jsonify({
                "agreed": float(agreed),
                "dissented": float(dissented),
                "notVoted": float(not_voted)
            }), 200
        else:
            return jsonify({"error": "MEP not found"}), 404

    except Error as e:
        current_app.logger.error(f"Database error: {e}")
        return jsonify({"error": str(e)}), 500
        

@meps.route("/mep/<int:mepID>/score", methods=['PUT'])
def update_mep_loyalty_score(mepID):
    current_app.logger.info('PUT /mep/<int:mepID>/score route entered')
    
    try:
        data = requests.json()
        
        required_fields = ["loyaltyScore"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        cursor = db.get_db().cursor()
        query = "UPDATE mep SET loyaltyScore, %s WHERE mepID = %s"

        cursor.execute(query, (data['loyaltyScore'], mepID))
        cursor.close()


        current_app.logger.info("PUT /mep/<int:mepID>/score route success")

        return (jsonify({"message": "MEP score successfully updated", "mepID": {mepID}, "loyaltyScore": data['loyaltyScore']}), 201,)

    except Error as e:
        return jsonify({"error": str(e)}), 500


@meps.route("/meps/<int:mepID>/party", methods=['GET'])
def get_mep_party(mepID):
    current_app.logger.info('GET /mep/<int:mepID>/party route entered')
    query = '''
        SELECT mep.partyID, partyName 
        FROM mep 
        JOIN political_party as p ON mep.partyID = p.partyID
        WHERE mepID = %s;
    '''
    cursor = db.get_db().cursor()

    cursor.execute(query, (mepID))
    retrieved_mep_party = cursor.fetchone()
    cursor.close()

    current_app.logger.info("GET /mep/<int:mepID>/party route success")
    response = make_response(jsonify(retrieved_mep_party))
    response.status_code = 200
    
    return response


@meps.route("/mep/<int:mepID>/picture", methods=['GET'])
def get_mep_photo(mepID):
    current_app.logger.info('GET /mep/<int:mepID>/picture route entered')
    query = '''
        SELECT photoURL 
        FROM mep 
        WHERE mepID = %s;
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query, (mepID,))
    retrieved_photo = cursor.fetchone()
    cursor.close()

    current_app.logger.info("GET /mep/<int:mepID>/picture route success")
    response = make_response(jsonify({"photoURL": retrieved_photo[0]}))
    response.status_code = 200
    
    return response
   


