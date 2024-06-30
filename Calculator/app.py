# app.py

from flask import Flask, render_template, request, jsonify
from calculator_backend import evaluate_expression

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    expression = request.form['expression']
    try:
        result = evaluate_expression(expression)
        return jsonify(result=str(result))
    except ValueError:
        return jsonify(result="Error")

if __name__ == '__main__':
    app.run(debug=True)
