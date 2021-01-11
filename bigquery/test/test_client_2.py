from unittest import TestCase

from bigquery.util.staging_utils import get_direct_exposure_query

class TestConfig(TestCase):

    def test_get_direct_exposure_query(self):

        direct_exposure_query = get_direct_exposure_query("direct_exposure", "34R3Bb2HErwvioRFa88HPVxBxx1SpAMeyd")
        expected_res = """(input_address = "34R3Bb2HErwvioRFa88HPVxBxx1SpAMeyd" or output_address = "34R3Bb2HErwvioRFa88HPVxBxx1SpAMeyd")"""
        print(direct_exposure_query)
        self.assertTrue(expected_res in direct_exposure_query)

    # def test_get_top_n_addresses_query(self):