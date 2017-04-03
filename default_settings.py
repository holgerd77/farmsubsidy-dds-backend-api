

API_VERSION = 'v1'

ELASTIC_HOST  = 'localhost:9200'
ELASTIC_INDEX = 'openfarmsubsidies'
ELASTIC_TYPE  = 'payment'
ELASTIC_URL   = 'http://{host}/{index}/{type}/'.format(
    host=ELASTIC_HOST,
    index=ELASTIC_INDEX,
    type=ELASTIC_TYPE)