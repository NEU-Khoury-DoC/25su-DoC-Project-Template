from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import db
from mysql.connector import Error
import numpy as np
from backend.ml_models.logistic import predict_gini

# Create a Blueprint for models routes
models = Blueprint("models", __name__)

# GET request to get a plotly prediction graph
@models.route("/predict/<int:graphID>", methods=["GET"])
def get_predictions(graphID):
    try:
        current_app.logger.info(f"Starting gini_plot request for GraphID {graphID}")
        cursor = db.get_db().cursor()

        # get the graph row
        cursor.execute("""SELECT XAxis, XMin, XMax, XStep, Population, GDP_per_capita, Trade_union_density, Corporate_tax_rate, Education, 
                       Health, Housing, Community_development, IRLT, Unemployment_rate,
                       Inflation, Region_East_Asia_and_Pacific, 
                       Region_Europe_and_Central_Asia, Region_Latin_America_and_Caribbean, 
                       Region_Middle_East_and_North_Africa  FROM Graphs WHERE GraphID = %s""", (graphID,))
        row = cursor.fetchone()
        current_app.logger.info(row)

        if row is None:
            return jsonify({"error": "Graph not found"}), 404

        # get weights of graph
        cursor.execute("""SELECT Population, GDP_per_capita, Trade_union_density, Corporate_tax_rate, Education, 
                       Health, Housing, Community_development, IRLT, Unemployment_rate,
                       Inflation, Region_East_Asia_and_Pacific, 
                       Region_Europe_and_Central_Asia, Region_Latin_America_and_Caribbean, 
                       Region_Middle_East_and_North_Africa 
                       FROM ModelWeights WHERE ModelName = 'Logistic Regression'""")
        weights = list(cursor.fetchone().values())
        current_app.logger.info(weights)

        # get describe metrics
        cursor.execute("""SELECT Population, GDP_per_capita, Trade_union_density, Corporate_tax_rate, Education, 
                       Health, Housing, Community_development, IRLT, Unemployment_rate,
                       Inflation, Region_East_Asia_and_Pacific, 
                       Region_Europe_and_Central_Asia, Region_Latin_America_and_Caribbean, 
                       Region_Middle_East_and_North_Africa  FROM PredictMetrics ORDER BY Metric""")
        rows = cursor.fetchall()
        

        cursor.close()

        columns = [col for col in rows[0].keys() if col != 'Metric']

        describe = [
            [row[col] for col in columns] for row in rows
            ]

        current_app.logger.info("describe")
        current_app.logger.info(describe)

        # get XAxis and range
        x_axis = row["XAxis"]
        x_min = row["XMin"]
        x_max = row["XMax"]
        x_step = row["XStep"]
        x_values = np.arange(x_min, x_max + x_step, x_step)

        gini_values = []

        current_app.logger.info(f"Predicting GINI for {len(x_values)} points")

        for x_val in x_values:
            x_input = row.copy()

            x_input[x_axis] = x_val
            
            x_input.pop("XAxis", None)
            x_input.pop("XMin", None)
            x_input.pop("XMax", None)
            x_input.pop("XStep", None)
            current_app.logger.info(x_axis)


            x_input = list(x_input.values())
            current_app.logger.info(x_input)

            current_app.logger.info(f"Predicting GINI for dfksdnfdnsfndsj points")
            gini = predict_gini(np.array(x_input), describe=np.array(describe), weights=np.array(weights), model="logistic")

            current_app.logger.info(f"Predicting FJDSOFJFJO for dfksdnfdnsfndsj points")
            gini_values.append(gini)

        output = {}
        output["predictions"] = gini_values
        output["x_axis"] = x_axis
        output["x_min"] = x_min
        output["x_max"] = x_max
        output["x_step"] = x_step

        return jsonify(output)

    except Exception as e:
        current_app.logger.error(f"Error in gini_plot: {str(e)}")
        return jsonify({"error": str(e)}), 500