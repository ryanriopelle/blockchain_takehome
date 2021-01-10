import pkgutil
import os

from bigquery.clients.bigquery_client import TrmBQClient
from bigquery.util.staging_utils import get_sql_from_file, reformat_query

# address, start_date, end_date, flow_type, limit, offset
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



