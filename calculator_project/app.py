# app.py
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    """Renders the main calculator HTML page."""
    return render_template('index.html')

if __name__ == '__main__':
    # Run the Flask app in debug mode for development.
    # This will typically open on http://127.0.0.1:5000/
    print("Starting Flask server. Open your browser to http://127.0.0.1:5000/")
    app.run(debug=True)

