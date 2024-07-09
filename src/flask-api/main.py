from flask import Flask, request
from flask_cors import CORS
import auth
import os
import get_value_range
import get_gasstation

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/health_check', methods=['GET'])
def health_check():
    return 'Im alive. Yay...'


@app.route("/")
def authenticate():
    return auth.validate()


# Get all prices from a specific gasstation
@app.route('/gasstation/<id>', methods=['GET'])
def _gasstation(id):
    return get_gasstation.run(id)


@app.route('/value_range', methods=['POST'])
def _get_value_range():
    json_data = request.get_json()
    gasstations = []
    for gasstation in json_data:
        gasstations.append(get_gasstation.run(gasstation))
    return get_value_range.run(gasstations)


host = os.getenv('API_IP_ADDRESS')
port = os.getenv('API_PORT')

if __name__ == "__main__":
    from waitress import serve
    serve(app, host=host, port=port)
