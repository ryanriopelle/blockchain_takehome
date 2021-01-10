import pkgutil

from google.cloud import bigquery
from google.cloud.bigquery import job as bq_job
from google.cloud.exceptions import Conflict

import os

client = bigquery.Client()


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


def make_initial_staging_table(query_string, dataset_name, table_name):
    """
    make first stage table
    :param query_string:
    :param dataset_name:
    :param table_name:
    :return:
    """
    config = bq_job.QueryJobConfig()
    config.write_disposition = 'WRITE_TRUNCATE'
    dataset_ref = client.dataset(dataset_name)
    table_ref = dataset_ref.table(table_name)
    config.destination = table_ref
    load_job = client.query(query_string, config)
    load_job.result()
    print("loaded {} rows".format(load_job.num_dml_affected_rows))


def reformat_query(query_string, dataset_name, env_name='trm-production'):
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


def append_table(query_text, source_dataset_name, table_name, target_dataset_name='bigquery-public-data'):
    """

    :param query_text:
    :param dataset_name:
    :param table_name:
    :return:
    """
    config = bq_job.QueryJobConfig()
    config.write_disposition = 'WRITE_APPEND'
    dataset_ref = client.dataset(target_dataset_name)
    table_ref = dataset_ref.table(table_name)
    config.destination = table_ref
    print('target = {}'.format(config.destination))
    query_string = reformat_query(query_text, source_dataset_name)
    load_job = client.query(query_string, config)
    return load_job


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