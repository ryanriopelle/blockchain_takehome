from unittest import TestCase

from bigquery.util.staging_utils import get_direct_exposure_query

class TestConfig(TestCase):

    def test_get_direct_exposure_query(self):

        direct_exposure_query = get_direct_exposure_query("direct_exposure", "34R3Bb2HErwvioRFa88HPVxBxx1SpAMeyd")
        expected_res = """
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
          (input_address = 34R3Bb2HErwvioRFa88HPVxBxx1SpAMeyd or output_address = 34R3Bb2HErwvioRFa88HPVxBxx1SpAMeyd) AND
          block_timestamp_month = DATE_TRUNC(CURRENT_DATE() , MONTH)
        """
        print(direct_exposure_query)
        self.assertEqual(direct_exposure_query, expected_res)


