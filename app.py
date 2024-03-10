from flask import Flask, request, jsonify, render_template, redirect
import json
import pandas as pd
import pickle
import joblib
import numpy as np
import hashlib
from random import random

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
    # importance[importance < 0.33] = 0
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


@app.route('/dataset', methods=['GET'])
def get_dataset():
    return redirect("https://home.in.tum.de/~deva/pseudo-fingerprinting/data.json")


@app.route('/fingerprint', methods=['POST'])
def calculate_hash():
    data = request.json
    df = pd.json_normalize(data, sep='_')
    df = df.reindex(columns=df_head.columns)

    for column in df.columns:
        try:
            for val in df[column].values:
                int(val)
        except:
            le = loaded_encoders[column]
            df[column] = safe_transform(le, df[column].astype(str))

    df.replace(-1, np.nan, inplace=True)

    # Get feature importance for KMeans
    feature_importance = feature_importance_kmeans(X_train)

    # Normalize the feature importance
    feature_importance /= np.sum(feature_importance)

    df.loc[1] = feature_importance
    # weighted_features = df.values * feature_importance
    weighted_features = []

    for i in range(len(df.values[0])):
        try:
            weighted_features.append(float(df.values[0][i]) * feature_importance[i])
        except:
            print("Could not process: ", df.values[0][i])

    fingerprint = (np.sum(weighted_features) * 1000) // 10 * 10

    pseuodofied = False

    if random() > 0.7:
        pseuodofied = True
        fingerprint += (((random() * (-1 if random() < 0.5 else 1)) * 100) // 10) * 10  # Add noise [-100; 100]

    # Create hash
    hash_object = hashlib.md5(fingerprint.tobytes())
    hash_value = hash_object.hexdigest()

    if pseuodofied:
        return str(hash_value) + ' (fake fingerprint)'
    return str(hash_value)


if __name__ == '__main__':
    app.run(debug=True, port=5000, host="0.0.0.0")
