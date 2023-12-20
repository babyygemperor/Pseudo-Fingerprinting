from flask import Flask, request, jsonify, render_template
import json

app = Flask(__name__)


@app.after_request
def add_headers(response):
    """
    Decorator function to add headers to the response.
    Allows cross-origin resource sharing (CORS) by setting the 'Access-Control-Allow-Origin',
    'Access-Control-Allow-Methods', and 'Access-Control-Allow-Headers' headers.
    """
    response.headers['Access-Control-Allow-Origin'] = '*'  # Allow requests from any origin
    response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'  # Allow POST and OPTIONS methods
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'  # Allow 'Content-Type' header
    return response


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/collect', methods=['POST'])
def collect_fingerprint():
    data = request.json
    json_str = json.dumps(data, indent=2)
    with open('data.json', 'a') as f:
        json.dump(data, f)
        f.write("\n")

    print("Received fingerprint data:", json_str)

    return jsonify({"status": "success", "message": "Data received"})


if __name__ == '__main__':
    app.run(debug=True, port=5000)
