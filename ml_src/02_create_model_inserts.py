import pandas as pd

#insert statements for model weights
df = pd.read_csv("ml-src/model_weights.csv")
columns = list(df.columns)
columns_sql = ", ".join(columns)

with open("database-files/02_insert_model_weights.sql", "w") as f:
    f.write("USE Consensus_DB; \n")
    for _, row in df.iterrows():
        values = []
        for col in columns:
            val = row[col]
            if isinstance(val, str):
                val = val.replace("'", "''")
                values.append(f"'{val}'")
            else:
                values.append(str(val))
        values_sql = ", ".join(values)
        insert_stmt = f"INSERT INTO ModelWeights ({columns_sql}) VALUES ({values_sql});\n"
        f.write(insert_stmt)

#insert statements for model mean and std
df = pd.read_csv("ml-src/describe.csv")
columns = list(df.columns)
columns_sql = ", ".join(columns)

with open("database-files/02_insert_model_weights.sql", "a") as f:
    for _, row in df.iterrows():
        values = []
        for col in columns:
            val = row[col]
            if isinstance(val, str):
                val = val.replace("'", "''")
                values.append(f"'{val}'")
            else:
                values.append(str(val))
        values_sql = ", ".join(values)
        insert_stmt = f"INSERT INTO PredictMetrics ({columns_sql}) VALUES ({values_sql});\n"
        f.write(insert_stmt)
