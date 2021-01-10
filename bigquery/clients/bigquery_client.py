import os
import logging

from contextlib import contextmanager
from typing import List

from google.cloud import bigquery
from google.cloud.bigquery.dataset import DatasetReference
from google.cloud.exceptions import NotFound as BQTableNotFound
from google.api_core.exceptions import BadRequest as BadRequest

from bigquery.config.trm_util_config import TrmUtilConfig

class TrmBQClient(object):

    def __init__(self, project=None):
        self._cfg = TrmUtilConfig()
        self._gcp_project = self._cfg.project_id
        self._client = self._cfg.client
        self._file_delimiter = '|'

    def dataset_ref(self, dataset_name):
        return DatasetReference(self._gcp_project, dataset_name)

    @property
    def gcp_project(self):
        return self._gcp_project

    @property
    def base_bq_client(self):
        return self._client

    @property
    def file_delimiter(self):
        return self._file_delimiter

    @file_delimiter.setter
    def file_delimiter(self, file_delimiter):
        self._file_delimiter = file_delimiter

    @staticmethod
    def gen_schema_from_list(columns_list: list) -> List[bigquery.schema.SchemaField]:
        """
        Generate BQ schema dict from lists of names & types
        :param columns_list: List of a list of "column name, datatype"
        :return: list of dict
        """

        schema = []
        fields = [{'type': dtype, 'field_name': tname, 'mode': 'NULLABLE'} for (tname, dtype) in columns_list]

        for field in fields:
            schema.append(bigquery.SchemaField(field['field_name'], field['type'], mode=field['mode']))

        return schema

    def get_schema_from_bq_api(self, table_ref: bigquery.table) -> List[bigquery.SchemaField]:
        try:
            table = self._client.get_table(table_ref)
            return table.schema

        except BQTableNotFound:
            return None

    def single_column_result_as_list(self, query_string: str, column_name: str) -> list:
        """

        :param query_string:
        :param column_name:
        :return:
        """
        query_job = self._client.query(query_string)
        results = query_job.result()
        return [row[column_name] for row in results]

    def query_job(self,
                  query_text: str,
                  query_params: List = None
                  ):
        if query_params is None:
            return self._client.query(query_text).result()
        else:
            job_config = bigquery.QueryJobConfig
            query_job_params = [bigquery.ScalarQueryParameter(k.get('name'),
                                                              k.get('datatype', 'STRING'),
                                                              k.get('value')) for k in query_params]
            job_config.query_parameters = query_job_params
            return self._client.query(query_text,
                                      location='US',
                                      job_config=job_config).result()

    def query_to_pandas_dataframe(self,
                                  query_text: str,
                                  query_params: List = None):
        """

        :param query_text: the text of the query to run
        :param target_file_name: target file path to write to
        :param colsep field delimiter
        :param query_params list of dicts with query params
        :return: None
        """

        try:
            df = self.query_job(query_text, query_params).to_dataframe()

        except IOError:
            import traceback
            logging.error(traceback.format_exc())
        except BadRequest:
            import traceback
            logging.error('passed invalid query')
            logging.error(traceback.format_exc())

        return df

    def query_to_local_file(self,
                            query_text: str,
                            target_file_name: str,
                            colsep: str = '|',
                            query_params: List = None,
                            header=True) -> None:
        """

        :param query_text: the text of the query to run
        :param target_file_name: target file path to write to
        :param colsep field delimiter
        :param query_params list of dicts with query params
        :return: None
        """
        print("Running query to localfile")
        try:
            df = self.query_to_pandas_dataframe(query_text, query_params)
            df.to_csv(target_file_name, sep=colsep, index=False, header=header)
            logging.info("saved file to csv")
        except IOError:
            import traceback
            logging.error(traceback.format_exc())
        except BadRequest:
            import traceback
            logging.error('passed invalid query')
            logging.error(traceback.format_exc())

    @contextmanager
    def query_to_temp_file(self,
                           query_text: str,
                           temp_file_name: str,
                           colsep: str = '|',
                           query_params: List = None,
                           header=True):
        """

        :param query_text:
        :param temp_file_name:
        :param colsep:
        :param query_params:
        :return:
        """
        yield self.query_to_local_file(query_text,
                                       temp_file_name,
                                       colsep,
                                       query_params,
                                       header)

        os.remove(temp_file_name)

    def list_tables_in_dataset(self, dataset_name: str = 'trm_sample_data') -> list:
        """
        list all tables in a dataset -- use to create list of tables to load
        :param dataset_name:
        :return: list
        """

        dataset_name = f'{self.gcp_project}.{dataset_name}'
        big_query_tables = self._client.list_tables(dataset_name)

        return [item.table_id for item in big_query_tables]
