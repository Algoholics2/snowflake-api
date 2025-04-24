# backend.py
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import snowflake.connector
import os
load_dotenv()

app = Flask(__name__)



# Connect to Snowflake
conn = snowflake.connector.connect(
    user=os.getenv('user'),
    password=os.getenv('password'),
    account=os.getenv('account'),
    warehouse='compute_wh',
    database='DOCUMENTS',
    schema='PUBLIC'
)

@app.route("/query", methods=["POST"])
def query_snowflake():
    sql_query = request.json.get("query")
    try:
        cursor = conn.cursor()
        cursor.execute(sql_query)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        results = [dict(zip(columns, row)) for row in rows]
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
