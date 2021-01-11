WITH address as
(select '1P75yv8CGeaRoX4x6M1iQvtAU6JhniUgDJ' addr),
flows as
(SELECT
  input_address AS sender,
  output_address AS receiver,
  -- Adjust value for decimals. Bitcoin has 10**8 decimals
  SUM(SAFE_DIVIDE(LEAST(input_value, output_value), POW(10, 8))) AS value,
FROM
  `bigquery-public-data.crypto_bitcoin.transactions`,
  UNNEST(inputs) AS input,
  UNNEST(input.addresses) AS input_address,
  UNNEST(outputs) AS output,
  UNNEST(output.addresses) AS output_address
WHERE
  -- Using partition column to reduce dataset size
  block_timestamp_month = DATE_TRUNC(CURRENT_DATE() , MONTH)
GROUP BY input_address,output_address),
inflows as (
SELECT addr,
       sender counterparty,
       sum(value) inflows,
       0 outflows
  FROM flows f join address a on (f.receiver = a.addr)
  GROUP BY 1,2
),
outflows as (
SELECT addr,
       receiver counterparty,
       0 inflows,
       sum(value) outflows,
  FROM flows f join address a on (f.sender = a.addr)
  group by 1, 2
)
SELECT addr,
       counterparty,
       sum(inflows) inflows,
       sum(outflows) outflows
  FROM (
        SELECT *
         FROM inflows
        UNION ALL
        SELECT *
         FROM outflows
  )
  GROUP BY 1, 2;