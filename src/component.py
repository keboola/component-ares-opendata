'''
Template Component main class.

'''

import csv
import logging
import os
import sys
from datetime import datetime
from pathlib import Path

from kbc.env_handler import KBCEnvHandler

from ares import opendata
from ares import parser

# configuration variables
KEY_URL_CFG = 'ares_url'

# #### Keep for debug
KEY_DEBUG = 'debug'

MANDATORY_PARS = []
MANDATORY_IMAGE_PARS = []

APP_VERSION = '0.0.1'


class Component(KBCEnvHandler):

    def __init__(self, debug=False):
        # for easier local project setup
        default_data_dir = Path(__file__).resolve().parent.parent.joinpath('data').as_posix() \
            if not os.environ.get('KBC_DATADIR') else None

        KBCEnvHandler.__init__(self, MANDATORY_PARS, data_path=default_data_dir,
                               log_level=logging.DEBUG if debug else logging.INFO)
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

    def run(self):
        '''
        Main execution code
        '''
        params = self.cfg_params  # noqa
        ares_url = params.get(KEY_URL_CFG, opendata.ARES_SET_URL)

        logging.info('Getting last update date of the ARES dataset.')
        last_update_date = opendata.get_current_export_date()
        get_new_file = True
        if self.get_state_file() and self.get_state_file().get('last_update'):
            last_dt_str = self.get_state_file().get('last_update')
            last_downloaded = datetime.strptime(last_dt_str, '%Y-%m-%d').date()
            get_new_file = last_update_date > last_downloaded

        if get_new_file:
            logging.info('Downloading last version of the ARES dataset..')
            root_folder = Path(self.data_path).parent
            result_file = root_folder.joinpath('tmp/ares_vreo_all.tar.gz')
            tar_file = opendata.download_ares_file(result_file, url=ares_url)
            logging.info('Parsing data..')
            parser.process_data(tar_file, self.tables_out_path)
        else:
            logging.warning(f"There's no new ARES dataset since last download, last update was on {last_update_date}")

        logging.info("Downloading the change set.")
        ico_change_set_path = Path(self.tables_out_path).joinpath('ico_change_set')
        opendata.download_ico_change_set(ico_change_set_path)
        self._add_change_date(ico_change_set_path, last_update_date)
        self.configuration.write_table_manifest(file_name=str(ico_change_set_path),
                                                primary_key=['ICO', 'CHANGE_DT'],
                                                columns=['ICO', 'CHANGE_DT', 'DATASET_UPDATED'])

        self.write_state_file({'last_update': str(last_update_date)})

        logging.info('Finished!')

    def _add_change_date(self, ico_change_set_path, last_update_date):
        files = ico_change_set_path.glob('*')
        for i, f in enumerate(files):
            f_name = f.name
            new_path = f.parent.joinpath(str(i) + '.csv')
            with open(f, 'r') as read_obj, \
                    open(new_path, 'w', newline='') as write_obj:
                # Create a csv.reader object from the input file object
                csv_reader = csv.reader(read_obj)
                # Create a csv.writer object from the output file object
                csv_writer = csv.writer(write_obj)
                # Read each row of the input csv file as list
                for row in csv_reader:
                    # Append the default text in the row / list
                    change_date = f_name.split('_')[1].split('.')[0]
                    row.append(str(datetime.strptime(change_date, '%Y%m%d').date()))
                    row.append(str(last_update_date))
                    # Add the updated row / list to the output file
                    csv_writer.writerow(row)
            os.remove(f)


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
