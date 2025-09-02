import requests
import json

# Replace with the actual URL of your deployed backend on Render
BACKEND_URL = "https://your-backend-url.onrender.com"

# Replace with the API key you generated and put in app.py
API_KEY = "95913a9c4ed84471ba04ce174bdf0dcb"

def add_new_certificate(cert_data):
    headers = {
        'Content-Type': 'application/json',
        'X-API-Key': API_KEY
    }
    try:
        response = requests.post(f"{BACKEND_URL}/add_certificate", data=json.dumps(cert_data), headers=headers)
        response.raise_for_status() # Raise an exception for bad status codes
        print(response.json())
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    # --- Example 1: Add a certificate with a partner ---
    new_cert_1 = {
        "cert_number": "NA-GSP-25-004",
        "name": "Alex Baker",
        "course": "Cybersecurity Fundamentals",
        "date": "Nov 2025",
        "partner": "CyberCorp",
        "portal": "Nelbion Academy",
        "summary": "Alex is an outstanding student with a strong foundation in network security."
    }
    add_new_certificate(new_cert_1)

    # --- Example 2: Add a certificate without a partner ---
    new_cert_2 = {
        "cert_number": "NA-GSP-25-005",
        "name": "Samantha Lee",
        "course": "Digital Marketing",
        "date": "Dec 2025",
        "partner": None, # Set partner to None
        "portal": "Nelbion Academy",
        "summary": "Samantha excelled in creating and analyzing digital campaigns."
    }
    add_new_certificate(new_cert_2)