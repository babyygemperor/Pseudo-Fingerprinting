from flask import Flask, request, jsonify, render_template
import json
import pandas as pd
import pickle
import joblib
import numpy as np
import hashlib

app = Flask(__name__)

with open('encoders.pkl', 'rb') as file:
    loaded_encoders = pickle.load(file)

with open('X_train.pkl', 'rb') as file:
    X_train = pickle.load(file)

with open('df_head.pkl', 'rb') as file:
    df_head = pickle.load(file)

model = joblib.load('KMeans_model.pkl')


def feature_importance_kmeans(data):
    # Find the distance of each feature from the cluster's center
    centers = model.cluster_centers_
    importance = np.std(data, axis=0) * np.sqrt(np.sum((centers - centers.mean(axis=0)) ** 2, axis=0))
    importance[importance < 0.33] = 0
    return importance


def safe_transform(le, series, default_value='unknown'):
    """
    Transforms the data using label encoder. If an unseen label is encountered,
    it is replaced with the default_value.
    """
    try:
        return le.transform(series)
    except ValueError as e:
        return 0


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

    return jsonify({"status": "success", "message": "Data received"})


@app.route('/fingerprint', methods=['POST'])
def calculate_hash():
    data = request.json
    df = pd.json_normalize(data, sep='_')
    df = df.reindex(columns=df_head.columns)

    for column in df.columns:
        if column in loaded_encoders:
            le = loaded_encoders[column]
            df[column] = safe_transform(le, df[column].astype(str))

    df.replace(-1, np.nan, inplace=True)

    # Get feature importance for KMeans
    feature_importance = feature_importance_kmeans(X_train)

    # Normalize the feature importance
    feature_importance /= np.sum(feature_importance)

    # Apply feature importance weights
    weighted_features = df.values * feature_importance

    # Create hash
    hash_object = hashlib.md5(weighted_features.tobytes())
    hash_value = hash_object.hexdigest()
    return hash_value


if __name__ == '__main__':
    app.run(debug=True, port=5000)
