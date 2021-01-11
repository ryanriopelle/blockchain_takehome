from flask import Flask, request, render_template, Response
from flask import abort, make_response, jsonify
import json
import sys, logging

from bigquery.util.staging_utils import get_data_from_query, get_direct_exposure_query, top_n_address_flows_query

logging.basicConfig(stream=sys.stderr, level=logging.INFO)
logger = logging.getLogger(__name__)
app = Flask(__name__)

@app.route('example_test_api/data',  methods=['GET'])
def example_test_api():

    sample_res = {
    "data": [
      {"address": "1FGhgLbMzrUV5mgwX9nkEeqHbKbUK29nbQ",
       "inflows": "0",
       "outflows": "0.01733177",
       "total_flows": "0.01733177"},
      {"address": "1Huro4zmi1kD1Ln4krTgJiXMYrAkEd4YSh",
       "inflows": "0.01733177",
       "outflows": "0",
       "total_flows": "0.01733177"},
    ],
    "success": True
    }
    return sample_res

@app.route('/transfers_data',  methods=['GET'])
def transfers_data():
    results = get_data_from_query()
    logger.info(f"results: {results}")
    return results


@app.route('/address/exposure/direct',  methods=['GET'])
def address_exposure_direct():
    if not address:
        abort(make_response(jsonify(status='error',
                                    message='Error: Need address'), 400))
    results = get_direct_exposure_query("direct_exposure", address)
    logger.info(f"results: {results}")
    return results


@app.route('/top_n_address_flows',  methods=['GET'])
def transfers_data():

    address  = request.args.get('address', '34R3Bb2HErwvioRFa88HPVxBxx1SpAMeyd')
    top_n = request.args.get('top_n', 25)
    flow_type = request.args.get('flow_type', 'both')
    start_date = request.args.get('start_date', '00:00:00')
    end_date = request.args.get('end_date', '00:00:00')

    if not address:
        abort(make_response(jsonify(status='error',
                                    message='Error: Need address'), 400))
    if not top_n:
        abort(make_response(jsonify(status='error',
                                    message='Error: Need top n (int)'), 400))
    if not flow_type:
        abort(make_response(jsonify(status='error',
                                    message='Error: Need flow_type'), 400))
    if not start_date:
        abort(make_response(jsonify(status='error',
                                    message='Error: Need start_date'), 400))
    if not end_date:
        abort(make_response(jsonify(status='error',
                                    message='Error: Need end_date'), 400))

    results = get_data_from_query()
    logger.info(f"results: {results}")
    return results


if __name__ == "__main__":
    app.run(host='0.0.0.0')