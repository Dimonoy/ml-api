import dill
import pandas as pd
import os
dill._dill._reverse_typemap['ClassType'] = type

import flask
import logging
from logging.handlers import RotatingFileHandler
from time import strftime


app = flask.Flask(__name__)
model = None

handler = RotatingFileHandler(filename='app.log', maxBytes=100000, backupCount=10)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)

def load_model(model_path):
	# load the pre-trained model
	global model
	with open(model_path, 'rb') as f:
		model = dill.load(f)
	print(model)

modelpath = "/app/app/models/logreg_pipeline.dill"
load_model(modelpath)

@app.route("/", methods=["GET"])
def general():
	return """Welcome to fraudelent prediction process. Please use 'http://<address>/predict' to POST"""

@app.route("/predict", methods=["POST"])
def predict():
	data = {"success": False}
	dt = strftime("[%Y-%b-%d %H:%M:%S]")
	if flask.request.method == "POST":

		description, company_profile, benefits = "", "", ""
		request_json = flask.request.get_json()
		if request_json["description"]:
			description = request_json['description']

		if request_json["company_profile"]:
			company_profile = request_json['company_profile']

		if request_json["benefits"]:
			benefits = request_json['benefits']
		logger.info(f'{dt} Data: description={description}, company_profile={company_profile}, benefits={benefits}')
		try:
			preds = model.predict_proba(pd.DataFrame({"description": [description],
												  "company_profile": [company_profile],
												  "benefits": [benefits]}))
		except AttributeError as e:
			logger.warning(f'{dt} Exception: {str(e)}')
			data['predictions'] = str(e)
			data['success'] = False
			return flask.jsonify(data)

		data["predictions"] = preds[:, 1][0]
		data["success"] = True

	return flask.jsonify(data)

if __name__ == "__main__":
	print(("* Loading the model and Flask starting server..."
		"please wait until server has fully started"))
	port = int(os.environ.get('PORT', 8180))
	app.run(host='0.0.0.0', debug=True, port=port)
