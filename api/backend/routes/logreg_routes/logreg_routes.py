from flask import Blueprint, jsonify
from flask import current_app
from backend.ml_models.logreg import predict

logreg_bp = Blueprint('customer', __name__, url_prefix='/l')


@logreg_bp.route('/prediction/<party>/<procedure_type>', methods=['GET'])
def get_prediction(party, procedure_type):
    try:
        # log inputs
        current_app.logger.info(f"Received prediction request for party={party}, procedure_type={procedure_type}")

        # call model prediction function
        result = predict(party, procedure_type)

        # return the result as json
        return jsonify({'prediction': round(result, 2)})

    except Exception as e:
        current_app.logger.error(f"Prediction error: {e}")
        return jsonify({'error': 'Prediction failed'}), 500
