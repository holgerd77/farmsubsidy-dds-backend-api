import json, requests
from flask import Flask, jsonify, make_response, request

import default_settings


app = Flask(__name__)
app.config.from_object(default_settings)

PAYMENTS_ENDPOINT = '/{version}/payments/'.format(version=app.config['API_VERSION'])


def build_query_dict(request):
    q_dict = { 'query': {
        'bool': {
            'must': [],
            'filter': [],
        }
    }}
    m = q_dict['query']['bool']['must']
    f = q_dict['query']['bool']['filter']
    
    q = request.args.get('q', '')
    if q != '':
        m.append({ 'match': { '_all': str(q) }})
    
    name = request.args.get('name', '')
    if name != '':
        f.append({ 'term': { 'name': str(name).lower() }})
    
    country = request.args.get('country', '')
    if country != '':
        f.append({ 'term': { 'country': str(country).lower() }})
    
    zip_code = request.args.get('zip_code', '')
    if zip_code != '':
        f.append({ 'term': { 'zip_code': str(zip_code).lower() }})
    
    town = request.args.get('town', '')
    if town != '':
        f.append({ 'term': { 'town': str(town).lower() }})
    
    return q_dict
    

@app.route(PAYMENTS_ENDPOINT, methods=['GET',])
def index():
    #q = request.args.get('q', '')
    q_dict = build_query_dict(request)
    payload = { 'source': json.dumps(q_dict), 'pretty': '' }
    r = requests.get(app.config['ELASTIC_URL'] + '_search', params=payload)
    if True or r.status_code == 200:
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