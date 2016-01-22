import requests
from flask import Flask, jsonify, make_response, request

import default_settings


app = Flask(__name__)
app.config.from_object(default_settings)

ENDPOINT_URL = '/{version}/payments/'.format(version=app.config['API_VERSION'])


@app.route(ENDPOINT_URL, methods=['GET',])
def index():
    q = request.args.get('q', '')
    payload = { 'q': q, 'pretty': '' }
    print(app.config['ELASTIC_URL'])
    r = requests.get(app.config['ELASTIC_URL'] + '_search', params=payload)
    if r.status_code == 200:
        return r.content
    else:
        e_dict = { 'error': { 'msg': 'An error occured', 'code': r.status_code } }
        return make_response(jsonify(e_dict), r.status_code)


@app.errorhandler(404)
def not_found(error):
    e_dict = { 'error': { 'msg': 'Page not found', 'code': 404 } }
    return make_response(jsonify(e_dict), 404)


if __name__ == '__main__':
    
    app.run(debug=True)