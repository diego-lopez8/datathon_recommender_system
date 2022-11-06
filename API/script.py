from flask import Flask, Request
import pickle
import numpy as np
app=Flask(__name__)
# prediction function
@app.route("/")
def ValuePredictor(to_predict_list):
	to_predict = np.array(to_predict_list).reshape(1, 12)
	loaded_model = pickle.load(open("model.pkl", "rb"))
	result = loaded_model.predict(to_predict)
	return result[0]

