import os
import yaml
import pkgutil

CONFIG_FILE = 'conf.yml'

class TRM_Configs(object):

    def __init__(self, conf_file=None):
        current_env = os.environ.get('ENVIRONMENT', 'development')
        project = os.environ.get('GCR_PROJECT', current_env)

        if conf_file is None:
            self._conf_file_name = CONFIG_FILE
        else:
            self._conf_file_name = conf_file

        ymlfile = pkgutil.get_data('bigquery.config', self.conf_file_name).decode('utf-8')
        cfg_all = yaml.load(ymlfile,  Loader=yaml.FullLoader)
        self.cfg = cfg_all.get(current_env)

    @property
    def conf_file_name(self):
        return self._conf_file_name