from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import db
from mysql.connector import Error
import numpy as np

# Create a Blueprint for playground routes
playground = Blueprint("playground", __name__)

# List of all feature variables from the database schema
FEATURE_VARIABLES = [
    'Population', 'GDP_per_capita', 'Trade_union_density', 'Unemployment_rate',
    'Health', 'Education', 'Housing', 'Community_development', 'Real_interest_rates',
    'Productivity', 'Corporate_tax_rate', 'Inflation', 'Personal_property_tax', 'IRLT',
    'Region_East_Asia_and_Pacific', 'Region_Europe_and_Central_Asia', 
    'Region_Latin_America_and_Caribbean', 'Region_Middle_East_and_North_Africa'
]

# POST request to generate GINI predictions for a graph
# Example: /playground/generate
@playground.route("/generate", methods=["POST"])
def generate_graph():
    try:
        current_app.logger.info("Starting generate_graph request")
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['x_axis', 'x_min', 'x_max', 'x_steps']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        x_axis = data['x_axis']
        x_min = float(data['x_min'])
        x_max = float(data['x_max'])
        x_steps = int(data['x_steps'])
        
        # Validate x_axis is a valid feature variable
        if x_axis not in FEATURE_VARIABLES:
            return jsonify({"error": f"Invalid x_axis variable: {x_axis}"}), 400
        
        # Validate feature values are provided for all variables
        feature_values = {}
        for feature in FEATURE_VARIABLES:
            if feature in data:
                try:
                    feature_values[feature] = float(data[feature])
                except (ValueError, TypeError):
                    return jsonify({"error": f"Invalid value for {feature}"}), 400
            else:
                return jsonify({"error": f"Missing feature value: {feature}"}), 400
        
        # Generate x values based on range and steps
        if x_steps <= 0:
            return jsonify({"error": "x_steps must be positive"}), 400
        
        if x_min >= x_max:
            return jsonify({"error": "x_min must be less than x_max"}), 400
        
        x_values = np.linspace(x_min, x_max, x_steps)
        
        # Generate predictions for each x value
        predictions = []
        for x_val in x_values:
            # Create feature vector with x_axis variable set to x_val
            features = feature_values.copy()
            features[x_axis] = x_val
            
            # TODO: Replace this placeholder with actual model prediction
            # For now, using a simple mock prediction based on feature values
            gini_prediction = predict_gini(features)
            
            predictions.append({
                'x': float(x_val),
                'y': float(gini_prediction)
            })
        
        current_app.logger.info(f"Successfully generated {len(predictions)} predictions")
        return jsonify({
            "predictions": predictions,
            "x_axis": x_axis,
            "x_min": x_min,
            "x_max": x_max,
            "x_steps": x_steps
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error in generate_graph: {str(e)}")
        return jsonify({"error": str(e)}), 500

# POST request to save a graph to the database
# Example: /playground/save
@playground.route("/save", methods=["POST"])
def save_graph():
    try:
        current_app.logger.info("Starting save_graph request")
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['user_id', 'name', 'x_axis', 'x_min', 'x_max', 'x_steps']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        user_id = int(data['user_id'])
        graph_name = data['name']
        x_axis = data['x_axis']
        x_min = float(data['x_min'])
        x_max = float(data['x_max'])
        x_steps = float(data['x_steps'])
        
        # Validate x_axis is a valid feature variable
        if x_axis not in FEATURE_VARIABLES:
            return jsonify({"error": f"Invalid x_axis variable: {x_axis}"}), 400
        
        # Validate and collect feature values
        feature_values = {}
        for feature in FEATURE_VARIABLES:
            if feature in data:
                try:
                    feature_values[feature] = float(data[feature])
                except (ValueError, TypeError):
                    return jsonify({"error": f"Invalid value for {feature}"}), 400
            else:
                return jsonify({"error": f"Missing feature value: {feature}"}), 400
        
        cursor = db.get_db().cursor()
        
        # Insert into Graphs table
        insert_graph_query = """
            INSERT INTO Graphs (XAxis, XMin, XMax, XStep, Population, GDP_per_capita, 
                              Trade_union_density, Unemployment_rate, Health, Education, 
                              Housing, Community_development, Real_interest_rates, 
                              Productivity, Corporate_tax_rate, Inflation, 
                              Personal_property_tax, IRLT, Region_East_Asia_and_Pacific, 
                              Region_Europe_and_Central_Asia, Region_Latin_America_and_Caribbean, 
                              Region_Middle_East_and_North_Africa)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        graph_values = (
            x_axis, x_min, x_max, x_steps,
            feature_values['Population'], feature_values['GDP_per_capita'],
            feature_values['Trade_union_density'], feature_values['Unemployment_rate'],
            feature_values['Health'], feature_values['Education'],
            feature_values['Housing'], feature_values['Community_development'],
            feature_values['Real_interest_rates'], feature_values['Productivity'],
            feature_values['Corporate_tax_rate'], feature_values['Inflation'],
            feature_values['Personal_property_tax'], feature_values['IRLT'],
            feature_values['Region_East_Asia_and_Pacific'], feature_values['Region_Europe_and_Central_Asia'],
            feature_values['Region_Latin_America_and_Caribbean'], feature_values['Region_Middle_East_and_North_Africa']
        )
        
        cursor.execute(insert_graph_query, graph_values)
        graph_id = cursor.lastrowid
        
        # Insert into SavedGraphs table
        insert_saved_graph_query = """
            INSERT INTO SavedGraphs (UserID, GraphID, Name)
            VALUES (%s, %s, %s)
        """
        cursor.execute(insert_saved_graph_query, (user_id, graph_id, graph_name))
        
        db.get_db().commit()
        cursor.close()
        
        current_app.logger.info(f"Successfully saved graph with ID {graph_id} for user {user_id}")
        return jsonify({
            "message": "Graph saved successfully",
            "graph_id": graph_id
        }), 201
        
    except Error as e:
        current_app.logger.error(f"Database error in save_graph: {str(e)}")
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        current_app.logger.error(f"Error in save_graph: {str(e)}")
        return jsonify({"error": str(e)}), 500

# GET request to retrieve saved graphs for a user
# Example: /playground/saved/123
@playground.route("/saved/<int:user_id>", methods=["GET"])
def get_saved_graphs(user_id):
    try:
        current_app.logger.info(f"Starting get_saved_graphs request for user {user_id}")
        cursor = db.get_db().cursor()
        
        # Get all saved graphs for the user with graph details
        query = """
            SELECT sg.Name, sg.DateTimeSaved, g.GraphID, g.XAxis, g.XMin, g.XMax, g.XStep,
                   g.Population, g.GDP_per_capita, g.Trade_union_density, g.Unemployment_rate,
                   g.Health, g.Education, g.Housing, g.Community_development, 
                   g.Real_interest_rates, g.Productivity, g.Corporate_tax_rate, g.Inflation,
                   g.Personal_property_tax, g.IRLT, g.Region_East_Asia_and_Pacific,
                   g.Region_Europe_and_Central_Asia, g.Region_Latin_America_and_Caribbean,
                   g.Region_Middle_East_and_North_Africa
            FROM SavedGraphs sg
            JOIN Graphs g ON sg.GraphID = g.GraphID
            WHERE sg.UserID = %s
            ORDER BY sg.DateTimeSaved DESC
        """
        
        cursor.execute(query, (user_id,))
        results = cursor.fetchall()
        
        saved_graphs = []
        for row in results:
            graph_data = {
                "name": row["Name"],
                "date_saved": row["DateTimeSaved"].isoformat() if row["DateTimeSaved"] else None,
                "graph_id": row["GraphID"],
                "x_axis": row["XAxis"],
                "x_min": row["XMin"],
                "x_max": row["XMax"],
                "x_steps": row["XStep"],
                "features": {
                    "Population": row["Population"],
                    "GDP_per_capita": row["GDP_per_capita"],
                    "Trade_union_density": row["Trade_union_density"],
                    "Unemployment_rate": row["Unemployment_rate"],
                    "Health": row["Health"],
                    "Education": row["Education"],
                    "Housing": row["Housing"],
                    "Community_development": row["Community_development"],
                    "Real_interest_rates": row["Real_interest_rates"],
                    "Productivity": row["Productivity"],
                    "Corporate_tax_rate": row["Corporate_tax_rate"],
                    "Inflation": row["Inflation"],
                    "Personal_property_tax": row["Personal_property_tax"],
                    "IRLT": row["IRLT"],
                    "Region_East_Asia_and_Pacific": row["Region_East_Asia_and_Pacific"],
                    "Region_Europe_and_Central_Asia": row["Region_Europe_and_Central_Asia"],
                    "Region_Latin_America_and_Caribbean": row["Region_Latin_America_and_Caribbean"],
                    "Region_Middle_East_and_North_Africa": row["Region_Middle_East_and_North_Africa"]
                }
            }
            saved_graphs.append(graph_data)
        
        cursor.close()
        
        current_app.logger.info(f"Retrieved {len(saved_graphs)} saved graphs for user {user_id}")
        return jsonify({
            "user_id": user_id,
            "saved_graphs": saved_graphs
        }), 200
        
    except Error as e:
        current_app.logger.error(f"Database error in get_saved_graphs: {str(e)}")
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        current_app.logger.error(f"Error in get_saved_graphs: {str(e)}")
        return jsonify({"error": str(e)}), 500

# GET request to retrieve a specific saved graph by graph_id
# Example: /playground/graph/456
@playground.route("/graph/<int:graph_id>", methods=["GET"])
def get_graph(graph_id):
    try:
        current_app.logger.info(f"Starting get_graph request for graph {graph_id}")
        cursor = db.get_db().cursor()
        
        query = """
            SELECT * FROM Graphs WHERE GraphID = %s
        """
        
        cursor.execute(query, (graph_id,))
        result = cursor.fetchone()
        
        if not result:
            return jsonify({"error": "Graph not found"}), 404
        
        graph_data = {
            "graph_id": result["GraphID"],
            "x_axis": result["XAxis"],
            "x_min": result["XMin"],
            "x_max": result["XMax"],
            "x_steps": result["XStep"],
            "features": {
                "Population": result["Population"],
                "GDP_per_capita": result["GDP_per_capita"],
                "Trade_union_density": result["Trade_union_density"],
                "Unemployment_rate": result["Unemployment_rate"],
                "Health": result["Health"],
                "Education": result["Education"],
                "Housing": result["Housing"],
                "Community_development": result["Community_development"],
                "Real_interest_rates": result["Real_interest_rates"],
                "Productivity": result["Productivity"],
                "Corporate_tax_rate": result["Corporate_tax_rate"],
                "Inflation": result["Inflation"],
                "Personal_property_tax": result["Personal_property_tax"],
                "IRLT": result["IRLT"],
                "Region_East_Asia_and_Pacific": result["Region_East_Asia_and_Pacific"],
                "Region_Europe_and_Central_Asia": result["Region_Europe_and_Central_Asia"],
                "Region_Latin_America_and_Caribbean": result["Region_Latin_America_and_Caribbean"],
                "Region_Middle_East_and_North_Africa": result["Region_Middle_East_and_North_Africa"]
            }
        }
        
        cursor.close()
        
        current_app.logger.info(f"Retrieved graph {graph_id}")
        return jsonify(graph_data), 200
        
    except Error as e:
        current_app.logger.error(f"Database error in get_graph: {str(e)}")
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        current_app.logger.error(f"Error in get_graph: {str(e)}")
        return jsonify({"error": str(e)}), 500

# GET request to get list of available feature variables
# Example: /playground/features
@playground.route("/features", methods=["GET"])
def get_features():
    try:
        current_app.logger.info("Starting get_features request")
        return jsonify({
            "features": FEATURE_VARIABLES
        }), 200
    except Exception as e:
        current_app.logger.error(f"Error in get_features: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Placeholder function for GINI prediction
# TODO: Replace this with your actual machine learning model
def predict_gini(features):
    """
    Placeholder function for GINI prediction using logistic regression model.
    
    Args:
        features (dict): Dictionary containing feature values
        
    Returns:
        float: Predicted GINI coefficient (0-1 scale)
    """
    # This is a placeholder implementation
    # Replace this with your actual trained model
    
    # Simple mock calculation for demonstration
    # In reality, you would load your trained model and make predictions
    base_gini = 0.3
    
    # Mock calculation using some features
    gdp_effect = (features.get('GDP_per_capita', 0) / 50000) * 0.1
    unemployment_effect = features.get('Unemployment_rate', 0) * 0.01
    education_effect = features.get('Education', 0) * -0.05
    
    predicted_gini = base_gini + gdp_effect + unemployment_effect + education_effect
    
    # Ensure GINI is within valid range (0-1)
    predicted_gini = max(0, min(1, predicted_gini))
    
    return predicted_gini

