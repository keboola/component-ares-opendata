'''
Template Component main class.

'''

import logging
import sys
from pathlib import Path

import requests
from kbc.env_handler import KBCEnvHandler

from ares import parser

# configuration variables
KEY_API_TOKEN = '#api_token'
ARES_SET_URL = 'http://wwwinfo.mfcr.cz/ares/ares_vreo_all.tar.gz'

# #### Keep for debug
KEY_DEBUG = 'debug'

MANDATORY_PARS = [KEY_API_TOKEN, KEY_API_TOKEN]
MANDATORY_IMAGE_PARS = []

APP_VERSION = '0.0.1'


class Component(KBCEnvHandler):

    def __init__(self, debug=False):
        KBCEnvHandler.__init__(self, MANDATORY_PARS, log_level=logging.DEBUG if debug else logging.INFO)
        # override debug from config
        if self.cfg_params.get(KEY_DEBUG):
            debug = True
        if debug:
            logging.getLogger().setLevel(logging.DEBUG)
        logging.info('Running version %s', APP_VERSION)
        logging.info('Loading configuration...')

        try:
            self.validate_config(MANDATORY_PARS)
            self.validate_image_parameters(MANDATORY_IMAGE_PARS)
        except ValueError as e:
            logging.exception(e)
            exit(1)
        # ####### EXAMPLE TO REMOVE
        # intialize instance parameteres

        # ####### EXAMPLE TO REMOVE END

    def run(self):
        '''
        Main execution code
        '''
        params = self.cfg_params  # noqa

        tar_file = self.__download_ares_file(ARES_SET_URL)
        parser.process_data(tar_file, self.tables_out_path)

        logging.info('Finished!')

    def __download_ares_file(self, url):
        # res = requests.get(url)
        # res.raise_for_status()
        root_folder = Path(self.data_path).parent
        result_file = root_folder.joinpath('tmp/ares_vreo_all.tar.gz')
        result_file.parent.mkdir(parents=True, exist_ok=True)
        # with open(result_file, 'wb+') as out:
        #     out.write(res.content)

        return result_file


"""
        Main entrypoint
"""
if __name__ == "__main__":
    if len(sys.argv) > 1:
        debug_arg = sys.argv[1]
    else:
        debug_arg = False
    try:
        comp = Component(debug_arg)
        comp.run()
    except Exception as exc:
        logging.exception(exc)
        exit(1)
