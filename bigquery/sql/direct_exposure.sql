-- Answer 1
SELECT
  sender,
  receiver,
  SUM(value) OVER (PARTITION BY sender, receiver) AS total_value,
  block_timestamp
FROM
(SELECT
  "btc" AS chain,
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
  (input_address = "<ADDRESS>" or output_address = "<ADDRESS>") AND
  block_timestamp_month = DATE_TRUNC(CURRENT_DATE() , MONTH)