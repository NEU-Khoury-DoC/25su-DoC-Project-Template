from flask import Blueprint, jsonify, request
from flask import current_app
from backend.ml_models.logreg import predict

logreg_bp = Blueprint('logreg', __name__)


@logreg_bp.route('/prediction', methods=['POST'])
def get_prediction():
    try:
        print("entering log reg routes")
        data = request.json
        print(data)


        # log inputs
        current_app.logger.info(f"Received prediction request for parties={data['parties']}, procedure_type={data['procedures']}")

        # call model prediction function
        result = predict(data['parties'], data['procedures'])

        # return the result as json
        return jsonify({'prediction': round(result, 2)})

    except Exception as e:
        current_app.logger.error(f"Prediction error: {e}")
        return jsonify({'error': 'Prediction failed'}), 500
