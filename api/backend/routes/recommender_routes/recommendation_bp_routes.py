from flask import Blueprint, jsonify, request
import pandas as pd
import numpy as np
import sqlite3
from backend.ml_models import new_recommender_cosine as recommender
import os

# Blueprint setup
recommender_bp = Blueprint('recommender_bp', __name__)

@recommender_bp.route('/recommender', methods=['GET'])
def recommend():
    try:
        # Validate required query parameters
        required_params = ['agree', 'attendance', 'party', 'party_pct', 'country', 'country_weight']
        missing = [p for p in required_params if request.args.get(p) is None]

        if missing:
            return jsonify({'error': f"Missing parameter(s): {', '.join(missing)}"}), 400

        # Get query parameters
        agree = float(request.args.get('agree'))
        attendance = float(request.args.get('attendance'))
        party = request.args.get('party')
        party_pct = float(request.args.get('party_pct'))
        country = request.args.get('country')
        country_weight = float(request.args.get('country_weight'))

        # Load CSV
        csv_path = os.path.join(os.getcwd(), 'backend/ml_models/active_members.csv')
        df = recommender.make_full_df(csv_path)

        # Generate weights
        weights = recommender.get_weights_vector(
            percent_agree_current_weight=5,
            percent_attendance_weight=90,
            my_party=party,
            my_party_percentage_weight=4,
            new_candidate_country_weight=country_weight
        )

        # Get top 10 recommendations
        recs_df = recommender.get_recommendations(
            df,
            agree,
            attendance,
            party,
            party_pct,
            new_candidate_country=country,
            weights=weights
        )

        return jsonify(recs_df.to_dict(orient='records'))

    except Exception as e:
        return jsonify({'error': str(e)}), 400

csv_path = os.path.join(os.getcwd(), 'backend/ml_models/active_members.csv')
belgium_df = pd.read_csv(csv_path)


@recommender_bp.route('/get-dissenters', methods=['GET'])
def get_dissenters_route():
    party_name = request.args.get('party_name')

    if not party_name:
        return jsonify({'error': 'Missing party_name parameter'}), 400

    # Copy the DataFrame to work with
    df = belgium_df.copy()

    # 🔍 Add these lines right here — before any filtering
    print("User is searching for party name:", party_name)
    print("Available party names in dataset:", df['party'].unique())

    # Now do the filtering (optionally more flexible with str.contains)
    df = df[df['party'].str.contains(party_name, case=False, na=False)]
    df = df[df['percent_agree_current'] != 0]

    df = df[['id', 'first_name', 'last_name', 'percent_dissent_current']]
    df = df.sort_values(by='percent_dissent_current', ascending=False)
    df = df.rename(columns={
        'id': 'MEP ID',
        'first_name': 'First Name',
        'last_name': 'Last Name',
        'percent_dissent_current': 'Dissent Rate'
    })

    dissents = df.head(10)

    return jsonify(dissents.to_dict(orient='records'))

@recommender_bp.route('/get-dissent-rate', methods=['GET'])
def get_dissent_rate():
    """
    Returns the dissent rate for a given MEP using only their unique ID.
    Query parameters:
        - id (str or int): MEP ID
    """
    mep_id = request.args.get('id')

    if not mep_id:
        return jsonify({'error': 'Missing id parameter'}), 400

    df = belgium_df.copy()

    # Filter by ID (convert to str in case of int/str mismatch)
    filtered = df[df['id'].astype(str) == str(mep_id)]

    if filtered.empty:
        return jsonify({'error': f'MEP with id {mep_id} not found'}), 404

    mep_data = filtered.iloc[0]
    return jsonify({
        'id': mep_id,
        'first_name': mep_data['first_name'],
        'last_name': mep_data['last_name'],
        'party': mep_data['party'],
        'dissent_rate': mep_data['percent_dissent_current']
    })

@recommender_bp.route('/get-country-heatmap', methods=['GET'])
def get_country_heatmap():
    try:
        # mapping from frontend names to csv names
        party_name_map = {
            "European People's Party": "European People’s Party",
            "Progressive Alliance of Socialists and Democrats": "Progressive Alliance of Socialists and Democrats",
            "Renew Europe": "Renew Europe",
            "Greens/European Free Alliance": "Greens/European Free Alliance",
            "The Left (GUE/NGL)": "The Left in the European Parliament – GUE/NGL",
            "European Conservatives and Reformists": "European Conservatives and Reformists",
            "Identity and Democracy": "Identity and Democracy",
            "Non-Inscrits": "Non-attached Members"
        }

        party_display = request.args.get('party')
        party = party_name_map.get(party_display)

        if not party:
            return jsonify({'error': f"Unsupported party: {party_display}"}), 400

        # load csv
        csv_path = os.path.join(os.getcwd(), 'backend/ml_models/active_members.csv')
        df = pd.read_csv(csv_path)

        # filter to selected party only
        df_party = df[df["party"] == party].copy()

        # country iso code mapping
        eu_countries = {
            'Austria': 'AUT', 'Belgium': 'BEL', 'Bulgaria': 'BGR', 'Croatia': 'HRV', 'Cyprus': 'CYP',
            'Czechia': 'CZE', 'Denmark': 'DNK', 'Estonia': 'EST', 'Finland': 'FIN', 'France': 'FRA',
            'Germany': 'DEU', 'Greece': 'GRC', 'Hungary': 'HUN', 'Ireland': 'IRL', 'Italy': 'ITA',
            'Latvia': 'LVA', 'Lithuania': 'LTU', 'Luxembourg': 'LUX', 'Malta': 'MLT', 'Netherlands': 'NLD',
            'Poland': 'POL', 'Portugal': 'PRT', 'Romania': 'ROU', 'Slovakia': 'SVK', 'Slovenia': 'SVN',
            'Spain': 'ESP', 'Sweden': 'SWE'
        }

        results = []

        for country, iso in eu_countries.items():
            df_country = df_party[df_party["country"] == country]

            if df_country.empty:
                continue

            avg_dissent = df_country["percent_dissent_current"].mean()

            if pd.isna(avg_dissent):
                continue

            loyalty_score = 1 - (avg_dissent / 100)

            results.append({
                "country": country,
                "iso_alpha": iso,
                "avg_dissent_rate": round(avg_dissent, 2),
                "match_score": round(loyalty_score * 100, 2)
            })

        return jsonify(results)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
