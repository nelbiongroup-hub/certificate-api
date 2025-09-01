from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 

DATABASE = 'certificates.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/verify', methods=['POST'])
def verify_certificate():
    data = request.json
    cert_number = data.get('cert_number')
    portal_id = data.get('portal_id')

    if not cert_number or not portal_id:
        return jsonify({"status": "error", "message": "Certificate number and portal ID are required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    # Query for the certificate
    cursor.execute(
        "SELECT * FROM certificates WHERE cert_number = ? AND portal = ?", 
        (cert_number, portal_id)
    )
    certificate_data = cursor.fetchone()
    
    conn.close()

    if certificate_data:
        # Certificate found, return the details including the new summary field
        details = {
            "name": certificate_data['name'],
            "course": certificate_data['course'],
            "date": certificate_data['date'],
            "partner": certificate_data['partner'],
            "portal": certificate_data['portal'],
            "summary": certificate_data['summary'] # New field
        }
        return jsonify({"status": "verified", "data": details})
    else:
        # Certificate not found
        return jsonify({"status": "not_found"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)