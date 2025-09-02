from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 

DATABASE = 'certificates.db'

# NOTE: For production, store this in an environment variable, not here.
API_KEY = "95913a9c4ed84471ba04ce174bdf0dcb" 

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Endpoint to add a NEW certificate
@app.route('/add_certificate', methods=['POST'])
def add_certificate():
    api_key_from_request = request.headers.get('X-API-Key')
    if api_key_from_request != API_KEY:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401

    data = request.json
    cert_number = data.get('cert_number')
    name = data.get('name')
    course = data.get('course')
    date = data.get('date')
    partner = data.get('partner')
    portal = data.get('portal')
    summary = data.get('summary')

    if not all([cert_number, name, course, date, portal]):
        return jsonify({"status": "error", "message": "Missing required fields"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute('''
            INSERT INTO certificates (cert_number, name, course, date, partner, portal, summary)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (cert_number, name, course, date, partner, portal, summary))
        conn.commit()
        return jsonify({"status": "success", "message": f"Certificate {cert_number} added successfully"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"status": "error", "message": f"Certificate {cert_number} already exists"}), 409
    finally:
        conn.close()

# New endpoint to UPDATE an existing certificate
@app.route('/update_certificate', methods=['PUT'])
def update_certificate():
    api_key_from_request = request.headers.get('X-API-Key')
    if api_key_from_request != API_KEY:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401
    
    data = request.json
    cert_number = data.get('cert_number')
    
    if not cert_number:
        return jsonify({"status": "error", "message": "Certificate number is required"}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Build the UPDATE query dynamically
    update_fields = []
    update_values = []
    
    # Check for each possible field to update
    if 'name' in data:
        update_fields.append("name = ?")
        update_values.append(data['name'])
    if 'course' in data:
        update_fields.append("course = ?")
        update_values.append(data['course'])
    if 'date' in data:
        update_fields.append("date = ?")
        update_values.append(data['date'])
    if 'partner' in data:
        update_fields.append("partner = ?")
        update_values.append(data['partner'])
    if 'portal' in data:
        update_fields.append("portal = ?")
        update_values.append(data['portal'])
    if 'summary' in data:
        update_fields.append("summary = ?")
        update_values.append(data['summary'])

    if not update_fields:
        return jsonify({"status": "error", "message": "No fields to update"}), 400
    
    query = f"UPDATE certificates SET {', '.join(update_fields)} WHERE cert_number = ?"
    update_values.append(cert_number)
    
    try:
        cursor.execute(query, update_values)
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"status": "error", "message": "Certificate not found"}), 404
        return jsonify({"status": "success", "message": f"Certificate {cert_number} updated successfully"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        conn.close()

# Existing /verify endpoint
@app.route('/verify', methods=['POST'])
def verify_certificate():
    data = request.json
    cert_number = data.get('cert_number')
    portal_id = data.get('portal_id')

    if not cert_number or not portal_id:
        return jsonify({"status": "error", "message": "Certificate number and portal ID are required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM certificates WHERE cert_number = ? AND portal = ?", 
        (cert_number, portal_id)
    )
    certificate_data = cursor.fetchone()
    
    conn.close()

    if certificate_data:
        details = {
            "name": certificate_data['name'],
            "course": certificate_data['course'],
            "date": certificate_data['date'],
            "partner": certificate_data['partner'],
            "portal": certificate_data['portal'],
            "summary": certificate_data['summary']
        }
        return jsonify({"status": "verified", "data": details})
    else:
        return jsonify({"status": "not_found"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)