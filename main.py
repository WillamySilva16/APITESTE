import os
import pymssql
from flask import Flask, jsonify

app = Flask(__name__)

DB_SERVER = os.getenv("DB_SERVER")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

@app.route("/")
def home():
    return "API online!"

@app.route("/dados")
def dados():
    conn = pymssql.connect(
        server=DB_SERVER,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=1433
    )
    cursor = conn.cursor(as_dict=True)
    cursor.execute("SELECT TOP 10 * FROM TAB_REGISTRO_VISITA_SUPERVISAO_CABECALHO")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
