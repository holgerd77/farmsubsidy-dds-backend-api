import json, requests
from flask import Flask, jsonify, make_response, request
from flask.ext.cors import CORS

import default_settings


app = Flask(__name__)
app.config.from_object(default_settings)
cors = CORS(app)

PAYMENTS_ENDPOINT = '/{version}/payments/'.format(version=app.config['API_VERSION'])
COUNTRIES_ENDPOINT = '/{version}/countries/'.format(version=app.config['API_VERSION'])


def build_query_dict(request):
    q_dict = {
        'sort': [ { 'amount_euro': 'desc' } ],
        'query': {
            'bool': { 'must': [], 'filter': [], } },
        'aggs': {
            'Towns': { 'terms' : { 'field' : 'town', 'size': 5 } },
            'Countries': { 'terms' : { 'field' : 'country', 'size': 5 } },
            'Years': { 'terms' : { 'field' : 'year', 'size': 5 } },
            'Sub Payments Type': { 'terms' : { 'field' : 'sub_payments_euro.name', 'size': 12 } }
        }
    }
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
        f.append({ 'term': { 'town': str(town) }})
    
    year = request.args.get('year', '')
    if year != '':
        f.append({ 'term': { 'year': int(year) }})
    
    amount_euro_gte = request.args.get('amount_euro_gte', '')
    if amount_euro_gte != '':
        f.append({ 'range': { 'amount_euro': { 'gte': float(amount_euro_gte) } }})
    
    sub_payments_type = request.args.get('sub_payments_type', '')
    if sub_payments_type != '':
        f.append({ 'term': { 'sub_payments_euro.name': str(sub_payments_type) }})
    
    return q_dict
    

@app.route(PAYMENTS_ENDPOINT, methods=['GET',])
def payments():
    #q = request.args.get('q', '')
    q_dict = build_query_dict(request)
    payload = { 'source': json.dumps(q_dict), 'pretty': '' }
    from_attr = request.args.get('start', '')
    if from_attr != '':
        payload['from'] = from_attr;
    size = request.args.get('rows', '')
    if size != '':
        payload['size'] = size;
    
    r = requests.get(app.config['ELASTIC_URL'] + '_search', params=payload)
    if True or r.status_code == 200:
        return make_response(r.content, r.status_code)
    else:
        e_dict = { 'error': { 'msg': 'An error occured', 'code': r.status_code } }
        return make_response(jsonify(e_dict), r.status_code)


@app.route(COUNTRIES_ENDPOINT, methods=['GET',])
def countries():
    try:
        with open('countries.json', 'r') as c_file:
            c_str = c_file.read()
            return make_response(c_str, 200)
    except EnvironmentError:
        e_dict = { 'error': { 'msg': 'An error occured', 'code': 500 } }
        return make_response(jsonify(e_dict), 500)


@app.errorhandler(404)
def not_found(error):
    e_dict = { 'error': { 'msg': 'Page not found', 'code': 404 } }
    return make_response(jsonify(e_dict), 404)


if __name__ == '__main__':
    
    app.run(debug=True)