from flask import Flask, request, jsonify, send_from_directory
from math import radians, cos, sin, sqrt, atan2
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Example coordinates for the campus
campus_latitude = 14.2122
campus_longitude = 76.4196
RADIUS = 0.5  # Radius in km for location verification

# Function to calculate distance between two coordinates
def get_distance(lat1, lon1, lat2, lon2):
    R = 6371.0  # Radius of Earth in kilometers
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance

@app.route('/verify-location', methods=['POST'])
def verify_location():
    data = request.json
    if not data or 'latitude' not in data or 'longitude' not in data:
        return jsonify({'status': 'error', 'message': 'Missing location data'}), 400

    try:
        user_latitude = float(data.get('latitude'))
        user_longitude = float(data.get('longitude'))
    except (TypeError, ValueError):
        return jsonify({'status': 'error', 'message': 'Invalid latitude or longitude'}), 400

    # Calculate distance
    distance = get_distance(campus_latitude, campus_longitude, user_latitude, user_longitude)
    
    if distance <= RADIUS:
        return jsonify({'status': 'success', 'message': 'Location verified'}), 200
    else:
        return jsonify({'status': 'error', 'message': 'You are outside the campus'}), 403

# Route to serve HTML files
@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('public', path)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
