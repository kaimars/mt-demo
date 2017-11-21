
from api import app, log

@app.route('/')
def index():
    log.info('index loaded')
    return 'Hello World!'


@app.route('/predict')
def predict():
    log.info('predict called')
    return 'TODO'
