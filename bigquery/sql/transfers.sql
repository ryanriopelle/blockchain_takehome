SELECT
  'btc' AS chain,
  block_timestamp,
  block_hash,
  input_address AS sender,
  output_address AS receiver,
  SAFE_DIVIDE(LEAST(input_value, output_value), POW(10, 8)) AS value,
FROM
  `bigquery-public-data.crypto_bitcoin.transactions`,
  UNNEST(inputs) AS input,
  UNNEST(input.addresses) AS input_address,
  UNNEST(outputs) AS output,
  UNNEST(output.addresses) AS output_address
WHERE
  block_timestamp_month = DATE_TRUNC(CURRENT_DATE() , MONTH)
LIMIT 10