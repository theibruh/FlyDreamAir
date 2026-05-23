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

# Booking page route - display booking form for selected flight
@app.route('/book/<flight_id>')
def book_flight(flight_id):
    """
    Show booking form for a specific flight
    - Gets flight_id from URL
    - Finds flight in JSON data
    - Displays booking form with flight details
    """
    # Load all flights
    all_flights = load_flight_data()
    
    # Find the flight with matching ID
    selected_flight = None
    for flight in all_flights:
        if flight['flight_id'] == flight_id:
            selected_flight = flight
            break
    
    # If flight not found, show error
    if not selected_flight:
        return "Flight not found", 404
    
    # Render booking page with flight details
    return render_template('booking.html', flight=selected_flight)

# Confirm booking route - process booking form and save to JSON
@app.route('/confirm_booking', methods=['POST'])
def confirm_booking():
    """
    Process booking form submission
    - Gets form data (passenger info, flight ID)
    - Generates unique booking ID
    - Calculates total price
    - Saves to bookings.json
    - Shows confirmation page
    """
    import random
    import string
    from datetime import datetime
    
    # Get form data
    flight_id = request.form.get('flight_id')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    passengers = int(request.form.get('passengers'))
    
    # Find the flight
    all_flights = load_flight_data()
    flight = None
    for f in all_flights:
        if f['flight_id'] == flight_id:
            flight = f
            break
    
    if not flight:
        return "Flight not found", 404
    
    # Generate unique booking ID (e.g., FDAABC1234)
    booking_id = 'FDA' + ''.join(random.choices(string.ascii_uppercase, k=3)) + ''.join(random.choices(string.digits, k=4))
    
    # Calculate total price
    total_price = flight['price'] * passengers
    
    # Create booking object
    booking = {
        'booking_id': booking_id,
        'flight_id': flight_id,
        'flight_details': flight,
        'passenger': {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'phone': phone
        },
        'passengers_count': passengers,
        'total_price': total_price,
        'booking_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'status': 'confirmed'
    }
    
    # Save to bookings.json
    try:
        with open('data/bookings.json', 'r') as f:
            bookings = json.load(f)
    except:
        bookings = []
    
    bookings.append(booking)
    
    with open('data/bookings.json', 'w') as f:
        json.dump(bookings, f, indent=2)
    
    print(f"Booking created: {booking_id}")
    
    # Show confirmation page
    return render_template('confirmation.html', booking=booking)

# Run the Flask app
if __name__ == '__main__':
    print("STARTING FLASK BACKEND")
    print(f"Loaded {len(load_flight_data())} flights from flight_data.json")
    app.run(debug=True, host='127.0.0.1', port=5000)