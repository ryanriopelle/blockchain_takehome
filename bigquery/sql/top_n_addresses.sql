-- Answer 2
SELECT
counterparty_address,
max(inflow) as inflow,
max(outflow) as outflow,
(ifnull(max(inflow), 0) + ifnull(max(outflow), 0)) as total_flow
FROM
(
Select
    counterparty_address,
    CASE WHEN sender = '1P75yv8CGeaRoX4x6M1iQvtAU6JhniUgDJ' then total_value
        ELSE NUll
        END AS outflow,
    CASE WHEN receiver = '1P75yv8CGeaRoX4x6M1iQvtAU6JhniUgDJ' then total_value
      ELSE NUll
      END AS inflow
FROM
(SELECT
  Distinct
  sender,
  receiver,
  CASE WHEN sender = '1P75yv8CGeaRoX4x6M1iQvtAU6JhniUgDJ' then receiver
       ELSE SENDER
       END AS counterparty_address,
  SUM(value) OVER (PARTITION BY sender, receiver) AS total_value,
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
  -- Using partition column to reduce dataset size
  block_timestamp_month = DATE_TRUNC(CURRENT_DATE() , MONTH))
WHERE sender = '1P75yv8CGeaRoX4x6M1iQvtAU6JhniUgDJ' or receiver = '1P75yv8CGeaRoX4x6M1iQvtAU6JhniUgDJ'
AND sender != receiver))
group by counterparty_address