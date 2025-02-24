from flask import Flask, request, jsonify
from pymongo import MongoClient
import datetime
from config import CONFIG

app = Flask(__name__)

# Konfigurasi MongoDB Atlas
try:
    client = MongoClient(CONFIG["MONGO_URI"], serverSelectionTimeoutMS=5000)
    db = client["assignment2_stage2_sic"]
    collection = db["sensors_data"]
    print("Koneksi ke MongoDB sukses!")
except Exception as e:
    print("Gagal konek ke MongoDB:", e)

@app.route("/post_data", methods=["POST"])
def post_data():
    try:
        data = request.get_json()
        data["timestamp"] = datetime.datetime.now()
        collection.insert_one(data)
        return jsonify({"message": "Data saved!", "data": str(data)}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)