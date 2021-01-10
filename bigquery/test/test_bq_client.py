from datetime import datetime

from google.cloud.exceptions import Conflict
from google.cloud.bigquery.schema import SchemaField

from bigquery.clients.bigquery_client import TrmBigQueryTable

from data_util.test import test_dataset_name, test_table_name

"""
        col_names = ['loan_uuid', 'int_column', 'date_column', 'float_column', 'str_col']
        int_cols = ['int_column']
        date_cols = ['date_column']
        float_cols = ['float_column']
        gen override
        out_schema = bq_client.gen_schema_from_col_list(col_names, 'STRING', override_col_types)

"""


class TestBQClient(object):

    curr_date = datetime.utcnow().strftime('%Y%m%d')
    ctas_stmt = f'select {curr_date} as sampval'

    def load_ctas(self, bq_client):
        try:
            bq_client.load_table_from_query(self.ctas_stmt, test_dataset_name, test_table_name)
        except Conflict:
            print(f"{test_dataset_name}.{test_table_name} already exists.  Skipping")

    def test_ctas(self, test_bq_client):

        self.load_ctas(test_bq_client)
        tab = TrmBigQueryTable(test_dataset_name, test_table_name)

        assert tab.tbl_exists() is True

    def test_query(self, test_bq_client):

        self.load_ctas(test_bq_client)
        query_stmt = f'select sampval from {test_dataset_name}.{test_table_name}'
        query_output = test_bq_client.single_column_result_as_list(query_stmt, 'sampval')

        assert str(query_output[0]) == self.curr_date

    def test_schema_override(self, test_bq_client):
        col_names = ['loan_uuid', 'int_column', 'date_column', 'float_column', 'str_col']
        int_cols = ['int_column']
        date_cols = ['date_column']
        float_cols = ['float_column']

        test_table = TrmBigQueryTable(test_dataset_name, test_table_name)

        test_table.override_types_dict('INTEGER', int_cols)
        test_table.override_types_dict('DATE', date_cols)
        test_table.override_types_dict('FLOAT', float_cols)

        schema = test_bq_client.gen_schema_from_col_list(col_names,
                                                         default_type='STRING',
                                                         type_override=test_table.type_override)

        assert schema == [SchemaField('loan_uuid', 'STRING', 'NULLABLE', None, ()),
                          SchemaField('int_column', 'INTEGER', 'NULLABLE', None, ()),
                          SchemaField('date_column', 'DATE', 'NULLABLE', None, ()),
                          SchemaField('float_column', 'FLOAT', 'NULLABLE', None, ()),
                          SchemaField('str_col', 'STRING', 'NULLABLE', None, ())]

    def test_query_to_temp_file(self, test_bq_client):
        temp_file_name = 'tempy.txt'

        with test_bq_client.query_to_temp_file(self.ctas_stmt,
                                               temp_file_name,
                                               '|') as nada_bada_bing:
            with open(temp_file_name, 'r') as filey:
                result_list = filey.readlines()
                resultses = result_list[1].strip()

            assert resultses == self.curr_date

    def test_query_load_job_to_self_table(self, test_bq_client):
        """
        run with:
        pytest test_bq_client.py::TestBQClient::test_query_load_job_to_self_table -s
        note that the -s flag prints outputs

        """
        self.load_ctas(test_bq_client)
        tab = TrmBigQueryTable(test_dataset_name, test_table_name)

        assert tab.tbl_exists() is True
        tab.load_self_from_query(query=f"select 'test_field' as test_column")

        print("new table_schema:",test_bq_client.get_schema_from_bq_api(tab._table_ref))
        assert(test_bq_client.get_schema_from_bq_api(tab._table_ref)) == [SchemaField('test_column', 'STRING', 'NULLABLE', None, ()), SchemaField('sampval', 'INTEGER', 'NULLABLE', None, ())]
