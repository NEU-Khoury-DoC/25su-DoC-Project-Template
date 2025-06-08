from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app
import json
import pandas as pd
from backend.tourism.reccomender_ml import get_top_5_recommendations
from backend.tourism.time_series_predictions import get_country_prediction

# Create a Blueprint for routes
tourism_bp = Blueprint("tourism", __name__)

# Get the data from the RoadQuality table
@tourism_bp.route("/roadquality", methods=["GET"])
def get_road_qualities():
    try:
        cursor = db.get_db().cursor()

        cursor.execute("SELECT * FROM RoadQuality;")
        data = cursor.fetchall()

        if not data:
            return jsonify({"error": "Data not found"}), 404
        
        cursor.close()
        return jsonify(data), 200
    
    except Error as e:
        return jsonify({"error": str(e)}), 500
    

# Get the data from the TourismPrioritization table
@tourism_bp.route("/tourismprioritization", methods=["GET"])
def get_tourism_prior():
    try:
        cursor = db.get_db().cursor()

        cursor.execute("SELECT * FROM TourismPrioritization;")
        data = cursor.fetchall()
        if not data:
            return jsonify({"error": "Data not found"}), 404
        
        cursor.close()
        return jsonify(data), 200
    
    except Error as e:
        return jsonify({"error": str(e)}), 500
    

# Get the data from the RoadDensity table
@tourism_bp.route("/roaddensity", methods=["GET"])
def get_road_density():
    try:
        cursor = db.get_db().cursor()

        cursor.execute("SELECT * FROM RoadDensity;")
        data = cursor.fetchall()
        if not data:
            return jsonify({"error": "Data not found"}), 404
        
        cursor.close()
        return jsonify(data), 200
    
    except Error as e:
        return jsonify({"error": str(e)}), 500
    

# Get the data from the AvgFuelPrice table
@tourism_bp.route("/avgfuelprice", methods=["GET"])
def get_fuel_price():
    try:
        cursor = db.get_db().cursor()

        cursor.execute("SELECT * FROM AvgFuelPrice;")
        data = cursor.fetchall()

        if not data:
            return jsonify({"error": "Data not found"}), 404
        
        cursor.close()
        return jsonify(data), 200
    
    except Error as e:
        return jsonify({"error": str(e)}), 500
    

# Get the data from the RoadSpending table
@tourism_bp.route("/roadspending", methods=["GET"])
def get_road_spending():
    try:
        cursor = db.get_db().cursor()

        cursor.execute("SELECT * FROM RoadSpending;")
        data = cursor.fetchall()

        if not data:
            return jsonify({"error": "Data not found"}), 404
        
        cursor.close()
        return jsonify(data), 200
    
    except Error as e:
        return jsonify({"error": str(e)}), 500
    

# Get the data from the PassengerCars table
@tourism_bp.route("/passengercars", methods=["GET"])
def get_pass_cars():
    try:
        cursor = db.get_db().cursor()

        cursor.execute("SELECT * FROM PassengerCars;")
        data = cursor.fetchall()

        if not data:
            return jsonify({"error": "Data not found"}), 404
        
        cursor.close()
        return jsonify(data), 200
    
    except Error as e:
        return jsonify({"error": str(e)}), 500
    

# Get the data from the Trips table
@tourism_bp.route("/trips", methods=["GET"])
def get_trips():
    try:
        cursor = db.get_db().cursor()

        cursor.execute("SELECT * FROM Trips;")
        data = cursor.fetchall()

        if not data:
            return jsonify({"error": "Data not found"}), 404
        
        cursor.close()
        return jsonify(data), 200
    
    except Error as e:
        return jsonify({"error": str(e)}), 500
    
@tourism_bp.route("/recommender/<int:fuel_price>/<int:road_density>/<int:trips>", methods=["GET"])
def recommender_model(fuel_price, road_density, trips):
    try:
        cursor = db.get_db().cursor()

        cursor.execute("""SELECT afp.Country AS Country, afp.FuelPriceYear AS Year, afp.Score AS FuelPriceScore,
                rd.Score AS RoadDensityScore, t.NumTrips AS NumTrips
            FROM AvgFuelPrice afp
            JOIN RoadDensity rd ON afp.Country = rd.Country
                AND afp.FuelPriceYear = rd.DataYear
            JOIN Trips t ON afp.Country = t.Country
                AND afp.FuelPriceYear = t.TripYear
            WHERE afp.FuelPriceYear = 2019 
                AND t.Duration = '1 night or over';""")
        data = cursor.fetchall()
        if not data:
            return jsonify({"error": "Data not found"}), 404
        
        #json_data = json.loads(data)

        merged_df = pd.DataFrame(data)

        user_input = {"fuel_price": fuel_price,
                      "traffic_time": road_density,
                      "tourism_num": trips}
        
        recommendations = get_top_5_recommendations(user_input, merged_df)

        recom_dict = recommendations.to_dict(orient="records")

        cursor.close()
        return jsonify(recom_dict), 200
    
    except Error as e:
        return jsonify({"error": str(e)}), 500
    

@tourism_bp.route("/timeseries/<string:country>", methods=["GET"])
def timeseries_lr_model(country):
    try:
        cursor = db.get_db().cursor()

        cursor.execute("""SELECT rs.Country AS Country, rs.SpendingYear, rs.GDP AS GDP, t.NumTrips
            FROM RoadSpending rs
            JOIN Trips t ON rs.Country = t.Country
                AND rs.SpendingYear = t.TripYear
            WHERE t.Duration = '1 night or over';""")
        
        data = cursor.fetchall()
        if not data:
            return jsonify({"error": "Data not found"}), 404

        merged_df = pd.DataFrame(data)

        user_input = {"country": country}
        
        model_results = get_country_prediction(user_input, merged_df)

        recom_dict = model_results.to_dict(orient="records")

        cursor.close()
        return jsonify(recom_dict), 200
    
    except Error as e:
        return jsonify({"error": str(e)}), 500