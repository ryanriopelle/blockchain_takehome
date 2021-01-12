from unittest import TestCase

from bigquery.util.staging_utils import get_direct_exposure_query, get_top_n_addresses_query, get_data_from_query

class TestConfig(TestCase):

    def test_get_direct_exposure_query(self):

        direct_exposure_query = get_direct_exposure_query("34R3Bb2HErwvioRFa88HPVxBxx1SpAMeyd", limit= "20")
        expected_res = """(input_address = "34R3Bb2HErwvioRFa88HPVxBxx1SpAMeyd" or output_address = "34R3Bb2HErwvioRFa88HPVxBxx1SpAMeyd")"""
        # print(direct_exposure_query)
        self.assertTrue(expected_res in direct_exposure_query)

    def test_get_top_n_addresses_query(self):

        top_n_addresses_query = get_top_n_addresses_query(address= "34R3Bb2HErwvioRFa88HPVxBxx1SpAMeyd", top_n=25,
                                                    flow_type="'outflow','inflow','both'", start_date='2021-01-01', end_date='2021-01-25')
        print(top_n_addresses_query)
        self.assertTrue("sender = '34R3Bb2HErwvioRFa88HPVxBxx1SpAMeyd' or receiver = '34R3Bb2HErwvioRFa88HPVxBxx1SpAMeyd'" in top_n_addresses_query)
        self.assertTrue("flow_type in ('outflow','inflow','both')" in top_n_addresses_query)
        self.assertTrue("limit 25" in top_n_addresses_query)
        self.assertTrue('DATE_TRUNC(DATE "2021-01-01", MONTH)' in top_n_addresses_query)
        self.assertTrue('TIMESTAMP(DATETIME "2021-01-01 00:00:00")' in top_n_addresses_query)


    def test_get_data_from_query(self):

        query_text = """
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
                CASE WHEN sender = '34R3Bb2HErwvioRFa88HPVxBxx1SpAMeyd' then total_value
                    ELSE NUll
                    END AS outflow,
                CASE WHEN receiver = '34R3Bb2HErwvioRFa88HPVxBxx1SpAMeyd' then total_value
                  ELSE NUll
                  END AS inflow
            FROM
            (SELECT
              Distinct
              sender,
              receiver,
              CASE WHEN sender = '34R3Bb2HErwvioRFa88HPVxBxx1SpAMeyd' then receiver
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
            WHERE block_timestamp_month between
              DATE_TRUNC(DATE "2021-01-01", MONTH)
              AND DATE_TRUNC(DATE "2021-01-25", MONTH)
            AND block_timestamp between
              TIMESTAMP(DATETIME "2021-01-01 00:00:00")
              AND TIMESTAMP(DATETIME "2021-01-25 00:00:00")
             ) WHERE
            sender = '34R3Bb2HErwvioRFa88HPVxBxx1SpAMeyd' or receiver = '34R3Bb2HErwvioRFa88HPVxBxx1SpAMeyd'
            AND sender != receiver
            ))
            group by counterparty_address
            order by total_flow desc
            limit 3)
            WHERE flow_type in ('outflow','inflow','both')
        """

        data_result = get_data_from_query(query_text)
        # This result actually changes over time so it wont be consistent
        # Just showing this as an example, I could use PyMock to mock the result.
        expected_result = {'data': [{'counterparty_address': '3EcyY4Qk4HXiMFGktR1XG1T4hs5zyGKb6c',
                                      'inflow': 0.0, 'outflow': 1.25578385, 'total_flow': 1.25578385, 'flow_type': 'outflow'},
                                     {'counterparty_address': '1A9V3MPSf3oovdZ1AwzdJLX6Bz7DnG6KsG',
                                      'inflow': 0.0, 'outflow': 1.25578385, 'total_flow': 1.25578385, 'flow_type': 'outflow'},
                                     {'counterparty_address': '1MWKZvhbYzL4s94JcDPAzdiwoEEb5xzXxL',
                                      'inflow': 0.0, 'outflow': 1.25578385, 'total_flow': 1.25578385, 'flow_type': 'outflow'}],
                            'success': True}
        self.assertEqual(type(data_result), dict)