from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import db
from mysql.connector import Error
import numpy as np
from backend.ml_models.logistic import predict_gini

# Create a Blueprint for models routes
models = Blueprint("post_utils", __name__)

# GET request to get a plotly prediction graph
@models.route("/models/<int: graphID>", methods=["GET"])
def get_predictions(graphID):
    try:
        current_app.logger.info(f"Starting gini_plot request for GraphID {graphID}")
        cursor = db.get_db().cursor(dictionary=True)

        # get the graph row
        cursor.execute("SELECT * FROM Graphs WHERE GraphID = %s", (graphID,))
        row = cursor.fetchone()
        cursor.close()

        if row is None:
            return jsonify({"error": "Graph not found"}), 404

        # get weights of graph
        cursor.execute("""SELECT Trade_union_density, Corporate_tax_rate, Education, 
                       Health, Housing, Community_development, IRLT, Unemployment_rate,
                       Population, GDP_per_capita, Inflation, Region_East_Asia_and_Pacific, 
                       Region_Europe_and_Central_Asia, Region_Latin_America_and_Caribbean, 
                       Region_Middle_East_and_North_Africa 
                       FROM ModelWeights WHERE ModelName = 'Logistic Regression'""")
        weights = cursor.fetchone()

        # get describe metrics
        cursor.execute("SELECT * FROM PredictMetrics ORDER BY Statistic")
        rows = cursor.fetchall()

        columns = [col for col in rows[0].keys() if col != 'Statistic']

        describe = [
            [row[col] for col in columns] for row in rows
            ]

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

            x_input.pop("GraphID", None)
            x_input.pop("XAxis", None)
            x_input.pop("XMin", None)
            x_input.pop("XMax", None)
            x_input.pop("XStep", None)

            gini = predict_gini(x_input, describe=describe, weights=weights, model="logistic")

            gini_values.append(gini)


        


# put this in frontend. just format it
        # fig = go.Figure(data=go.Scatter(
        #     x=x_values,
        #     y=gini_values,
        #     mode='lines+markers',
        #     name='GINI Prediction'
        # ))

        # fig.update_layout(
        #     title=f"GINI vs {x_axis} (GraphID {graphID})",
        #     xaxis_title=x_axis,
        #     yaxis_title="Predicted GINI",
        #     template="plotly_white"
        # )

        current_app.logger.info("Returning plot")
        return jsonify({})

    except Exception as e:
        current_app.logger.error(f"Error in gini_plot: {str(e)}")
        return jsonify({"error": str(e)}), 500