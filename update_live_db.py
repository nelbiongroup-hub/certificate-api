import requests
import json

# Replace with the actual URL of your deployed backend on Render
BACKEND_URL = "https://your-backend-url.onrender.com"

# Replace with the API key you generated and put in app.py
API_KEY = "95913a9c4ed84471ba04ce174bdf0dcb"

def update_certificate_data(cert_data):
    headers = {
        'Content-Type': 'application/json',
        'X-API-Key': API_KEY
    }
    try:
        response = requests.put(f"{BACKEND_URL}/update_certificate", data=json.dumps(cert_data), headers=headers)
        response.raise_for_status()
        print(response.json())
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    # Correct the 'course' and add a 'partner' for an existing certificate
    update_data = {
        "cert_number": "NA-GSP-25-003",
        "course": "Advanced Web Development", # Corrected course title
        "partner": "Nelbion Academy", # Partner was previously None
        "summary": "Jane's performance was excellent. This certificate has been updated with a new course title and a partner."
    }
    update_certificate_data(update_data)