from flask import Flask, jsonify
import pytds
import os

app = Flask(__name__)

DB_SERVER = os.getenv("DB_SERVER")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

@app.route("/")
def home():
    return {"status": "API rodando!"}

@app.route("/dados")
def get_dados():
    try:
        with pytds.connect(
            server=DB_SERVER,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            port=1433,
            encrypt=True,
            trust_server_certificate=False
        ) as conn:

            cursor = conn.cursor()
            cursor.execute("SELECT TOP 100 * FROM TAB_REGISTRO_VISITA_SUPERVISAO_CABECALHO")
            rows = cursor.fetchall()

            columns = [col[0] for col in cursor.description]

            dados = [dict(zip(columns, row)) for row in rows]

            return jsonify(dados)

    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
