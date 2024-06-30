# flask_app.py
from flask import Flask, redirect
from url_shortener import get_long_url

app = Flask(__name__)

@app.route('/<short_url>')
def redirect_to_long_url(short_url):
    long_url = get_long_url(short_url)
    if long_url:
        return redirect(long_url)
    return 'URL not found', 404

if __name__ == '__main__':
    app.run(debug=True)
