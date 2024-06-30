from flask import Flask, request, redirect, jsonify, render_template_string
import sqlite3

from url_shortener import save_url, get_long_url

app = Flask(__name__)

# HTML template for the form
form_html = '''
<!DOCTYPE html>
<html>
<head>
    <title>URL Shortener</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css">
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.11.0/umd/popper.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"></script>
</head>
<body>
    <div class="container">
        <h1 class="mt-5">URL Shortener</h1>
        <form method="POST" action="/" class="mt-3">
            <div class="form-group">
                <label for="long_url">Enter the long URL:</label>
                <input type="text" class="form-control" id="long_url" name="long_url" required>
            </div>
            <button type="submit" class="btn btn-primary">Shorten</button>
        </form>
        {% if short_url %}
        <script>
            $(document).ready(function(){
                $('#shortUrlModal').modal('show');
            });
        </script>
        <div class="modal fade" id="shortUrlModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
            <div class="modal-dialog" role="document">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="exampleModalLabel">Short URL</h5>
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                    <div class="modal-body">
                        <p>Short URL: <a href="{{ short_url }}" target="_blank">{{ short_url }}</a></p>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                    </div>
                </div>
            </div>
        </div>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def home():
    short_url = None
    if request.method == 'POST':
        long_url = request.form['long_url']
        short_url = request.host_url + save_url(long_url)
    return render_template_string(form_html, short_url=short_url)

@app.route('/<short_url>')
def redirect_to_long_url(short_url):
    long_url = get_long_url(short_url)
    if long_url:
        return redirect(long_url)
    return 'URL not found', 404

if __name__ == '__main__':
    app.run(debug=True)
