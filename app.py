# Flask Backend 

from flask import Flask, render_template, request
import json

app = Flask(__name__)

def load_flight_data():
    with open('data/flights.json', 'r') as f:
        return json.load(f)
    
@app.route('/')
def index():
    flight_data = load_flight_data()
    return render_template('index.html', flights=flight_data)

# Search route - filter flights based on user input
@app.route('/search', methods=['POST'])
def search_flights():
    """
    Filter flights based on search criteria
    - Gets form data (origin, destination, date)
    - Filters flights.json
    - Returns matching flights
    """
    # Get form data from the search form
    origin = request.form.get('origin')
    destination = request.form.get('destination')
    date = request.form.get('date')
    
    # Load all flights
    all_flights = load_flight_data()
    
    # Filter flights that match search criteria
    filtered_flights = []
    for flight in all_flights:
        if (flight['origin'] == origin and 
            flight['destination'] == destination and 
            flight['date'] == date):
            filtered_flights.append(flight)
    
    # Render same page with filtered results
    return render_template('index.html', 
                         flights=filtered_flights,
                         search_performed=True,
                         origin=origin,
                         destination=destination,
                         date=date)

# Run the Flask app
if __name__ == '__main__':
    print("STARTING FLASK BACKEND")
    print(f"Loaded {len(load_flight_data())} flights from flight_data.json")
    app.run(debug=True, host='127.0.0.1', port=5000)