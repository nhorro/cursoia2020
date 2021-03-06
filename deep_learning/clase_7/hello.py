import numpy as np

from tensorflow import keras
from tensorflow.keras import layers
import joblib

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask import render_template


app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})

# load the model on server startup
dl_model = keras.models.load_model('models/model_embed.h5')
scaler = joblib.load('models/scaler.pkl')
vendor_id2idx = joblib.load('models/vendor_id2idx.pkl')

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/test')
def test():
    # test model with one prediction
    x_test = np.array([0.23333333, 0.30666667, 0.1626506 , 0.25540275, 0.06644518, 0.02430556, 0.39631336, 0.47708082, 0.34108527, 0.08988764, 0.20289855, 0. , 1. ])
    vendor_idx_test = np.array([28])
    prediction = dl_model.predict([x_test.reshape(1,-1), vendor_idx_test.reshape(1,1)])
    prediction = np.where(prediction > 0.5, 1, 0)
    truth = 0

    print(dl_model.summary())
    return 'La verdadera categoria del vino es {} y la predicción es {}'.format(truth, prediction)


@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    print(data)

    # TODO
    # Use data to build x_test and vendor_idx_test
    # Use the model to get the prediction (0 or 1)
    # Be careful with NaNs, min, max, and data types
    # Transform the prediction and return it to the front-end
    json_data = json.loads(request.get_json())
    # print(json_data)
    feats = np.array(json_data["features"]).reshape(1, -1)
    vendor_id = int(json_data["vendor_id"])
    decoded_vendor_id = vendor_id2idx[vendor_id]

    prediction = dl_model.predict([feats.reshape(1,-1), decoded_vendor_id])
    prediction = np.where(prediction > 0.5, 1, 0)

    prediction = 'low' if prediction < 0.5 else 'high'

    return {'quality': prediction}
