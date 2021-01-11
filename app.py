from flask import Flask, request, render_template, Response
from flask import abort, make_response, jsonify
import json
import sys, logging

from bigquery.util.staging_utils import get_data_from_query, get_direct_exposure_query, top_n_address_flows_query

logging.basicConfig(stream=sys.stderr, level=logging.INFO)
logger = logging.getLogger(__name__)
app = Flask(__name__)

@app.route('/address/exposure/direct',  methods=['GET'])
def address_exposure_direct():
    address  = request.args.get('address', 'fake_address')
    start_date = request.args.get('start_date', '0001-01-01T00:00:00Z')
    end_date = request.args.get('end_date', '9999-12-31T23:59:59Z')
    flow_type = request.args.get('flow_type', 'both')
    limit = request.args.get('limit', 100)
    offset = request.args.get('offset', 1.0)

    if not address:
        abort(make_response(jsonify(status='error',
                                    message='Error: Need address'), 400))
    if not start_date:
        abort(make_response(jsonify(status='error',
                                    message='Error: Need start_date'), 400))
    if not end_date:
        abort(make_response(jsonify(status='error',
                                    message='Error: Need end_date'), 400))
    if not flow_type:
        abort(make_response(jsonify(status='error',
                                    message='Error: Need flow_type'), 400))
    if not limit:
        abort(make_response(jsonify(status='error',
                                    message='Error: Need limit'), 400))
    if not offset:
        abort(make_response(jsonify(status='error',
                                    message='Error: Need offset'), 400))

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


@app.route('/direct_exposure',  methods=['GET'])
def direct_exposure():
    if not address:
        abort(make_response(jsonify(status='error',
                                    message='Error: Need address'), 400))
    results = get_direct_exposure_query("direct_exposure", address)
    logger.info(f"results: {results}")
    return results
#
#
# @app.route('/top_n_address_flows',  methods=['GET'])
# def transfers_data():
#
#     if not address:
#     abort(make_response(jsonify(status='error',
#                                 message='Error: Need address'), 400))
#     if not top_n:
#         abort(make_response(jsonify(status='error',
#                                     message='Error: Need top n (int)'), 400))
#     if not flow_type:
#         abort(make_response(jsonify(status='error',
#                                     message='Error: Need flow_type'), 400))
#     if not start_date:
#     abort(make_response(jsonify(status='error',
#                                 message='Error: Need start_date'), 400))
#     if not end_date:
#     abort(make_response(jsonify(status='error',
#                                 message='Error: Need end_date'), 400))
#
#     results = get_data_from_query()
#     logger.info(f"results: {results}")
#     return results


if __name__ == "__main__":
    app.run(host='0.0.0.0')