from flask import Flask, request, render_template, Response
from flask import abort, make_response, jsonify
import json
import sys, logging, datetime

from bigquery.util.staging_utils import run_query_for_file, get_data_from_query, get_direct_exposure_query, get_top_n_addresses_query

logging.basicConfig(stream=sys.stderr, level=logging.INFO)
logger = logging.getLogger(__name__)
app = Flask(__name__)

@app.route('/test_api/data',  methods=['GET'])
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

@app.route('/transfers',  methods=['GET'])
def transfers_data():
    results = run_query_for_file()
    logger.info(f"results: {results}")
    return results


@app.route('/address/exposure/direct',  methods=['GET'])
def address_exposure_direct():
    address = request.args.get('address')
    limit = request.args.get('limit', 20)
    if not address:
        abort(make_response(jsonify(status='error',
                                    message='Error: Need address'), 400))
    query_text = get_direct_exposure_query(address, limit)
    results = get_data_from_query(query_text)
    logger.info(f"results: {results}")
    return results


@app.route('/address/top_n_address_flows',  methods=['GET'])
def top_n_address_flows():

    address  = request.args.get('address')
    top_n = request.args.get('top_n', 25)
    _flow_type = request.args.get('flow_type', "any")
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    if not address:
        abort(make_response(jsonify(status='error',
                                    message='Error: Need address'), 400))
    if not top_n:
        abort(make_response(jsonify(status='error',
                                    message='Error: Need top n (int)'), 400))
    if not _flow_type:
        abort(make_response(jsonify(status='error',
                                    message='Error: Need flow_type'), 400))
    if not start_date:
        abort(make_response(jsonify(status='error',
                                    message='Error: Need start_date'), 400))
    if not end_date:
        abort(make_response(jsonify(status='error',
                                    message='Error: Need end_date'), 400))

    if _flow_type == "all" or _flow_type == "any":
        flow_type = "'outflow','inflow','both'"
    elif _flow_type == "outflow" or _flow_type =="inflow" or _flow_type =="both":
        flow_type = f"'{_flow_type}'"
    else:
        abort(make_response(jsonify(status='error',
                                    message='Error: choose flow type or any'), 400))

    format = "%Y-%m-%d"
    try:
        datetime.datetime.strptime(start_date, format)
        datetime.datetime.strptime(end_date, format)
        logger.info("This is the correct date string format.")
    except ValueError:
        abort(make_response(jsonify(status='error',
                                    message='Error: This is the incorrect date string format. It should be YYYY-MM-DD'), 400))

    query_text = get_top_n_addresses_query(address, top_n, flow_type, start_date, end_date)
    results = get_data_from_query(query_text)
    logger.info(f"results: {results}")
    return results


if __name__ == "__main__":
    app.run(host='0.0.0.0')