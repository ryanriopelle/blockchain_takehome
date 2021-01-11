import pkgutil

# from google.cloud import bigquery
# from google.cloud.bigquery import job as bq_job
# from google.cloud.exceptions import Conflict
from bigquery.clients.bigquery_client import TrmBQClient

import os

# client = bigquery.Client()


def init_env(env, creds_path):
    """
    set the environment variables for the bigquery client
    :param env: (string) development or production
    :param creds_path:
    :return:
    """
    os.environ['ENVIRONMENT'] = env
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = creds_path


def get_sql_from_file(file_name):
    """
    for sql files in "adhoc" directory, return the base SQL
    :param file_name:
    :return: String
    """
    return pkgutil.get_data('bigquery.sql', '{}.sql'.format(file_name))


def create_dataset(dataset_name):
    """
     um, create a dataset
    :param dataset_name:
    :return:
    """
    dataset_ref = client.dataset(dataset_name)
    dataset = bigquery.Dataset(dataset_ref)
    dataset.location = 'US'
    try:
        dataset = client.create_dataset(dataset)
    except Conflict:
        print("dataset {} already exists".format(dataset_name))
    except Exception:
        print("caught exception")
        import traceback
        traceback.format_exc()


def drop_table(dataset_name, table_name):
    """

    :param dataset_name:
    :param table_name:
    :return:
    """
    dataset_ref = client.dataset(dataset_name)
    table_ref = dataset_ref.table(table_name)
    table = bigquery.Table(table_ref)
    client.delete_table(table)


def reformat_query(query_string, dataset_name ='crypto_bitcoin', env_name='trm-production'):
    """
    helper -- replace placeholder strings
    :param query_string:
    :param dataset_name:
    :param env_name:
    :return:
    """
    import os
    environment_name = '-'.join(['trm', os.environ.get('ENVIRONMENT', 'production')])
    return query_string.replace('XXXPROJECTNAMEXXX', environment_name)\
        .replace('XXXSTAGINGDATASETXXX', dataset_name)\
        .replace('XXXRPTSTGXXX', 'rpt_staging')


def local_csv_to_bq(filepath, dataset_name, table_name, write_dispo='WRITE_TRUNCATE', file_delim=',', schema=None):
    job_config = bigquery.LoadJobConfig()
    if schema is None:
        job_config.autodetect = True
    else:
        job_config.schema=schema
    job_config.write_disposition = write_dispo
    dataset_ref = client.dataset(dataset_name)
    table_ref = dataset_ref.table(table_name)
    job_config.destination = table_ref
    job_config.source_format = bigquery.job.SourceFormat.CSV
    job_config.field_delimiter = file_delim
    job_config.skip_leading_rows = 1
    with open(filepath, 'rb') as source_file:
        job = client.load_table_from_file(
            source_file,
            table_ref,
            location='US',  # Must match the destination dataset location.
            job_config=job_config)  # API request
    job.result()  # Waits for table load to complete.
    print('Loaded {} rows into {}:{}.'.format(job.output_rows, dataset_name, table_name))


def run_query_for_file(sql_file: str = "transfers"):

    sql_text = get_sql_from_file(sql_file)
    encoding = 'utf-8'
    query_text = reformat_query(sql_text.decode(encoding))

    bq_client = TrmBQClient()
    data_res = bq_client.query_to_pandas_dataframe(query_text)
    return data_res.to_json(orient='records')


def get_direct_exposure_query(address, limit):
    """
    helper -- replace placeholder strings
    :param address: in format "34R3Bb2HErwvioRFa88HPVxBxx1SpAMeyd"
    :return:
    """
    sql_file: str = "direct_exposure"
    sql_text = get_sql_from_file(sql_file)
    encoding = 'utf-8'
    query_text = reformat_query(sql_text.decode(encoding))
    return query_text.replace('<ADDRESS>', address).replace('<LIMIT>', limit)


def get_top_n_addresses_query(address, top_n, flow_type,
                              start_date, end_date):

    """
    helper -- replace placeholder strings
    :param query_string:
    :param dataset_name:
    :param env_name:
    :return:
    """
    sql_file: str = "top_n_addresses"
    sql_text = get_sql_from_file(sql_file)
    encoding = 'utf-8'
    query_text = reformat_query(sql_text.decode(encoding))
    top_n = str(top_n)
    return query_text.replace('<ADDRESS>', address).replace('<TOP_N>', top_n).replace('<FLOW_TYPE>',flow_type).\
                      replace('<START_DATE>', start_date).replace('<END_DATE>', end_date)


def get_data_from_query(query_text):

    bq_client = TrmBQClient()
    data_res = bq_client.query_to_pandas_dataframe(query_text)
    return data_res.to_json(orient='records')