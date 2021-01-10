import os, sys
import yaml
import pkgutil
import logging
from google.cloud import bigquery
from google.oauth2 import service_account


# import os
# print(os.environ['PYTHONPATH'].split(os.pathsep))

CONFIG_FILE = 'conf.yml'
ENVIRONMENT = os.environ.get('ENVIRONMENT', 'development')
logging.basicConfig(stream=sys.stderr, level=logging.INFO)


class TrmUtilConfig(object):

    def __init__(self, conf_file: str = None):

        self.ENVIRONMENT = ENVIRONMENT
        self.cred_file = '/Users/ryanriopelle/Desktop/trm_labs_interview/trm-takehome-ryan-r-4d97f62c91b2.json'
        self.credentials = service_account.Credentials.from_service_account_file(self.cred_file)
        self.project_id = 'trm-takehome-ryan-r'
        self.client = bigquery.Client(credentials=self.credentials, project=self.project_id)



        # if conf_file is None:
        #     self._conf_file_name = CONFIG_FILE
        # else:
        #     self._conf_file_name = conf_file
        # # ymlfile = pkgutil.get_data('data_util.config', self.conf_file_name)
        # ymlfile = open(self.conf_file_name, 'r')
        # print(ymlfile, type(ymlfile))
        # cfg_all = yaml.load(ymlfile, Loader=yaml.UnsafeLoader)
        # self.cfg = cfg_all.get(self.ENVIRONMENT)
        # self.GCP_PROJECT = f'trm-{self.ENVIRONMENT}'