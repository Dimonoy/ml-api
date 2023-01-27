import os
import dill
import flask
import pathlib
import logging
import warnings

import pandas as pd

from time import strftime
from logging.handlers import RotatingFileHandler


dill._dill._reverse_typemap['ClassType'] = type
warnings.filterwarnings('ignore')

APP_ROOT_PATH = pathlib.Path('/rest-api')

LOG_FILE = 'app.log'
LOG_FILE_PATH = APP_ROOT_PATH / 'app' / pathlib.Path(LOG_FILE)
LOG_FILE_MAX_BYTES = 100_000
LOG_FILE_BACKUP_COUNT = 10

MODEL_FILE = 'logreg_pipeline.dill'
MODEL_FILE_PATH = APP_ROOT_PATH / 'app/models' / pathlib.Path(MODEL_FILE)

HOST = '0.0.0.0'
PORT = os.environ.get('PORT', 8180)
DEBUG = True

class Logger:
    def __init__(self, log_file, max_bytes, backup_count):
        self._handler = RotatingFileHandler(
            filename=str(log_file),
            maxBytes=max_bytes,
            backupCount=backup_count
        )
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(self._handler)

class Model:
    def __init__(self, model_path):
        self.model = None
        self.model_path = str(model_path)
        self.datetime = strftime('[%Y-%b-%d %H:%M:%S]')

    def load_model(self):
        assert os.path.exists(self.model_path), "File path is not valid. File does not exist!"

        with open(self.model_path, 'rb') as f:
            self.model = dill.load(f)

        return self
    
    def predict(self):
        data = {'success': None}

        if flask.request.method == 'POST':
            description, company_profile, benefits = '', '', ''
            request_json = flask.request.get_json()

            if request_json['description']:
                description = request_json['description']

            if request_json['company_profile']:
                company_profile = request_json['company_profile']

            if request_json['benefits']:
                benefits = request_json['benefits']

            logger.logger.info(
                f'{self.datetime} Data: description={description}, '
                f'company_profile={company_profile}, '
                f'benefits={benefits}'
            )

            try:
                predictions = model.model.predict_proba(
                    pd.DataFrame({
                        'description': [description],
                        'company_profile': [company_profile],
                        'benefits': [benefits],
                    })
                )
            except AttributeError as error:
                logger.logger.warning(f'{self.datetime} Exception: {str(error)}')

                data['error'] = str(error)
                data['success'] = False

                return flask.jsonify(data)
            
            data['predictions'] = predictions[:, 1][0]
            data['success'] = True

        return flask.jsonify(data)

if __name__ == "__main__":
    app = flask.Flask(__name__)
    logger = Logger(
        log_file=LOG_FILE_PATH,
        max_bytes=LOG_FILE_MAX_BYTES,
        backup_count=LOG_FILE_BACKUP_COUNT
    )
    model = Model(
        model_path=MODEL_FILE_PATH
    ).load_model()

    @app.route('/', methods=['GET'])
    def root():
        return """Welcome to prediction process. Please, use 'https://host/predict' to POST."""
    
    @app.route('/predict', methods=['POST'])
    def predict():
        data_json = model.predict()
        return data_json
    
    app.run(host=HOST, debug=DEBUG, port=PORT)
