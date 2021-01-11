-- Answer 2
SELECT counterparty_address, inflow, outflow, total_flow, flow_type
FROM (
SELECT
counterparty_address,
IFNULL(max(inflow), 0)  as inflow,
IFNULL(max(outflow), 0) as outflow,
(ifnull(max(inflow), 0) + ifnull(max(outflow), 0)) as total_flow,
CASE WHEN IFNULL(max(inflow), 0) = 0 then "outflow"
     WHEN IFNULL(max(outflow), 0) = 0 then "inflow"
     ELSE "both"
END AS flow_type
FROM
(
Select
    counterparty_address,
    CASE WHEN sender = '<ADDRESS>' then total_value
        ELSE NUll
        END AS outflow,
    CASE WHEN receiver = '<ADDRESS>' then total_value
      ELSE NUll
      END AS inflow
FROM
(SELECT
  Distinct
  sender,
  receiver,
  CASE WHEN sender = '<ADDRESS>' then receiver
       ELSE SENDER
       END AS counterparty_address,
  SUM(value) OVER (PARTITION BY sender, receiver) AS total_value,
  block_timestamp_month
FROM
(SELECT
  "btc" AS chain,
  block_timestamp,
  block_hash,
  input_address AS sender,
  output_address AS receiver,
  -- Adjust value for decimals. Bitcoin has 10**8 decimals
  SAFE_DIVIDE(LEAST(input_value, output_value), POW(10, 8)) AS value,
  block_timestamp_month
FROM
  `bigquery-public-data.crypto_bitcoin.transactions`,
  UNNEST(inputs) AS input,
  UNNEST(input.addresses) AS input_address,
  UNNEST(outputs) AS output,
  UNNEST(output.addresses) AS output_address
WHERE
block_timestamp_month = DATE_TRUNC(CURRENT_DATE() , MONTH))
WHERE block_timestamp_month >= DATE_TRUNC(DATE "<START_DATE>", MONTH)
AND block_timestamp_month <= DATE_TRUNC(DATE "<END_DATE>", MONTH)
AND sender = '<ADDRESS>' or receiver = '<ADDRESS>'
AND sender != receiver
))
group by counterparty_address
order by total_flow desc
limit <TOP_N>)
WHERE flow_type in (<FLOW_TYPE>)