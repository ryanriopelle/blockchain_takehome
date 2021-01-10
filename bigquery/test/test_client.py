import pkgutil
import os

from bigquery.clients.bigquery_client import TrmBQClient
from bigquery.util.staging_utils import get_sql_from_file, reformat_query

# address, start_date, end_date, flow_type, limit, offset
from bigquery.util.staging_utils import get_data_from_query


data = get_data_from_query()
print(data)