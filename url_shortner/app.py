from flask import Flask, request, redirect, render_template
import secrets
import threading
import webbrowser
import time
import os

# Initialize the Flask application
app = Flask(__name__)

# In-memory dictionary to store URL mappings.
# For a production application, you would use a persistent database (e.g., SQLite, PostgreSQL).
url_mappings = {} # Stores {short_code: long_url} pairs

@app.route('/')
def index():
    """
    Renders the main page of the URL shortener.
    This function is called when a user accesses the root URL ("/").
    """
    # Flask will look for 'index.html' in the 'templates' folder by default.
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def shorten_url():
    """
    Handles the URL shortening request.
    This function is called when the form on the main page is submitted.
    It generates a unique short code and stores the mapping.
    """
    long_url = request.form.get('long_url') # Use .get() to safely retrieve form data

    if not long_url:
        # If the URL is empty, render the index page with an error message.
        return render_template('index.html', short_url=None, error="Please enter a URL.")

    # Generate a unique short code.
    # secrets.token_urlsafe(6) generates a random, URL-safe text string of 6 characters.
    # We loop to ensure the generated code is truly unique in our current mappings.
    while True:
        short_code = secrets.token_urlsafe(6)
        if short_code not in url_mappings:
            break

    # Store the mapping: short code points to the long URL
    url_mappings[short_code] = long_url
    
    # Construct the full short URL that will be displayed to the user.
    # request.host_url gives the base URL (e.g., http://127.0.0.1:5000/)
    short_url = request.host_url + short_code

    # Render the index page again, passing the newly generated short URL to display it.
    return render_template('index.html', short_url=short_url)

@app.route('/<short_code>')
def redirect_to_long_url(short_code):
    """
    Handles redirection from a short URL to the original long URL.
    This function is called when a user accesses a short URL (e.g., http://127.0.0.1:5000/xyz123).
    """
    # Retrieve the original long URL using the short code
    long_url = url_mappings.get(short_code)

    if long_url:
        # If the long URL is found, redirect the user's browser to it.
        return redirect(long_url)
    else:
        # If the short code is not found, display an error page with a 404 status.
        return render_template('error.html'), 404

# Function to automatically open the web browser when the Flask server starts.
def open_browser():
    # Give the server a moment to fully initialize before trying to open the browser.
    time.sleep(1) 
    # Open a new tab in the default web browser pointing to the app's address.
    webbrowser.open_new_tab("http://127.0.0.1:5000")

if __name__ == '__main__':
    # This block ensures the code runs only when the script is executed directly (not imported as a module).

    # Start the browser opening function in a separate thread.
    # This allows the Flask server to start concurrently without being blocked.
    threading.Thread(target=open_browser).start()

    print("Starting URL Shortener server...")
    print("Access the application at: http://127.0.0.1:5000")
    print("Press Ctrl+C to stop the server.")
    
    # Run the Flask application.
    # debug=True enables debug mode, which provides detailed error messages and automatic reloading
    # of the server when code changes are detected. Set to False for production.
    app.run(debug=True)
