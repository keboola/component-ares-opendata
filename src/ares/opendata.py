import os
from datetime import datetime

import py7zr
import requests

ARES_VREO_URL = 'http://wwwinfo.mfcr.cz/ares/vreo.json'
ARES_SET_URL = 'http://wwwinfo.mfcr.cz/ares/ares_vreo_all.tar.gz'
ARES_ICO_CHANGESET_URL = 'http://wwwinfo.mfcr.cz/ares/ares_seznamIC_VR_zmen.7z'


def download_ares_file(result_file, url=ARES_SET_URL):
    res = requests.get(url, stream=True)
    res.raise_for_status()
    result_file.parent.mkdir(parents=True, exist_ok=True)
    with open(result_file, 'wb+') as out:
        for chunk in res.iter_content(chunk_size=8192):
            if chunk:  # filter out keep-alive new chunks
                out.write(chunk)

    return result_file


def get_current_export_date():
    """
    Returns date of lates update
    :return:
    """
    res = requests.get(ARES_VREO_URL)
    datum = res.json()['vreo'][0]['datumAktualizace']
    return datetime.strptime(datum, '%Y-%m-%d').date()


def download_ico_change_set(result_folder_path):
    res = requests.get(ARES_ICO_CHANGESET_URL, stream=True)
    res.raise_for_status()
    result_folder_path.mkdir(parents=True, exist_ok=True)
    result_file = os.path.join(result_folder_path, 'ico_change.7z')
    with open(result_file, 'wb+') as out:
        for chunk in res.iter_content(chunk_size=8192):
            if chunk:  # filter out keep-alive new chunks
                out.write(chunk)

    # extract
    archive = py7zr.SevenZipFile(result_file, mode='r')
    archive.extractall(path=result_folder_path)
    archive.close()
    os.remove(result_file)

    return result_folder_path
