from unittest import TestCase

from bigquery.util.staging_utils import get_direct_exposure_query, get_top_n_addresses_query, get_data_from_query

class TestConfig(TestCase):

    def test_get_direct_exposure_query(self):

        direct_exposure_query = get_direct_exposure_query("34R3Bb2HErwvioRFa88HPVxBxx1SpAMeyd")
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
        self.assertTrue('TIMESTAMP(DATETIME "2021-01-01 00:00:00")' in top_n_addresses_query)
        self.assertTrue('TIMESTAMP(DATETIME "2021-01-25 00:00:00")' in top_n_addresses_query)
