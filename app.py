# Flask Backend 

from flask import Flask, render_template
import json

app = Flask(__name__)

def load_flight_data():
    with open('data/flights.json', 'r') as f:
        return json.load(f)
    
@app.route('/')
def index():
    flight_data = load_flight_data()
    return render_template('index.html', flights=flight_data)

# Run the Flask app
if __name__ == '__main__':
    print("STARTING FLASK BACKEND")
    print(f"Loaded {len(load_flight_data())} flights from flight_data.json")
    app.run(debug=True, host='127.0.0.1', port=5000)