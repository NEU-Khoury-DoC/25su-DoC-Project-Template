from flask import Blueprint, jsonify, request
import pandas as pd
import numpy as np
import os

from backend.ml_models.recommender_cosine import (
    make_df, get_metrics, get_encoded_df,
    get_filters, get_recommendations
)

# Blueprint setup
recommendation = Blueprint('recommendation', __name__)

# Test route
@recommendation.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Recommendation route active"}), 200

@recommendation.route('/generate', methods=['POST'])
def generate_recommendation():
    try:
        # Parse incoming JSON
        data = request.get_json()

        # Required fields from frontend
        percent_agree_current = data.get("percent_agree_current")
        percent_attendance = data.get("percent_attendance")
        my_party = data.get("my_party")
        my_party_percentage = data.get("my_party_percentage")
        candidate_party = data.get("candidate_party")
        candidate_country = data.get("candidate_country")

        # Safety check
        if None in [percent_agree_current, percent_attendance, my_party, my_party_percentage, candidate_party, candidate_country]:
            return jsonify({"error": "Missing required input fields"}), 400

        # Load data
        full_df = make_df("backend/ml_models/members_cleaned.csv") 
        metrics_df = get_metrics(full_df, my_party)
        encoded_df = get_encoded_df(metrics_df)

        # Generate input vector and recommendations
        filters_vec = get_filters(percent_agree_current, percent_attendance, my_party, my_party_percentage, candidate_party, candidate_country)
        top_meps = get_recommendations(full_df, encoded_df, filters_vec, my_party)

        # Convert to dict format for frontend
        # Convert to native Python types
        recommendations = top_meps.to_dict(orient='records')

        # Recursively convert NumPy types to built-in Python types
        for rec in recommendations:
            for k, v in rec.items():
                if isinstance(v, (np.generic, np.ndarray)):
                    rec[k] = v.item() if hasattr(v, 'item') else float(v)

        return jsonify({"recommendations": recommendations}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
