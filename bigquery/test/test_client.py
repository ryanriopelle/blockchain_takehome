from google.cloud import bigquery
from google.oauth2 import service_account
credentials = service_account.Credentials.from_service_account_file('/Users/ryanriopelle/Desktop/trm_labs_interview/trm-takehome-ryan-r-4d97f62c91b2.json')

project_id = 'trm-takehome-ryan-r'
client = bigquery.Client(credentials= credentials,project=project_id)

query_job = client.query("""SELECT
  'btc' AS chain,
  block_timestamp,
  block_hash, 
  input_address AS sender,
  output_address AS receiver,
  -- Adjust value for decimals. Bitcoin has 10**8 decimals
  SAFE_DIVIDE(LEAST(input_value, output_value), POW(10, 8)) AS value, 
FROM
  `bigquery-public-data.crypto_bitcoin.transactions`,
  UNNEST(inputs) AS input,
  UNNEST(input.addresses) AS input_address,
  UNNEST(outputs) AS output,
  UNNEST(output.addresses) AS output_address
WHERE
  -- Using partition column to reduce dataset size
  block_timestamp_month = DATE_TRUNC(CURRENT_DATE() , MONTH)
LIMIT 10""")
results = query_job.result()

for row in results:
    print(row)
# print("results:", results)

