import os.path
import shutil

import scrapy
from SingleLog.log import Logger

logger = Logger('utils')


def save_page(domain, response: scrapy.http.Response, temp: bool = False):
    url = response.url
    if not url.startswith(domain):
        return

    file_name = f"../ptt_web/{url[len(domain):]}"

    file_path = file_name[:file_name.rfind('/') + 1]
    if not os.path.exists(file_path):
        os.makedirs(file_path, exist_ok=True)

    if temp:
        temp_file_name = f"./temp/{url[len(domain):]}"
        if not os.path.exists(temp_file_name):
            return

        if os.path.exists(file_name):
            os.remove(temp_file_name)
            return

        shutil.move(temp_file_name, file_name)
        logger.info('save page', temp_file_name, file_name)
    else:
        with open(file_name, 'w') as f:
            f.write(response.text)



def save_temp(domain, response: scrapy.http.Response):
    url = response.url
    if not url.startswith(domain):
        return

    temp_file_name = f"./temp/{url[len(domain):]}"

    file_path = temp_file_name[:temp_file_name.rfind('/') + 1]

    if not os.path.exists(file_path):
        os.makedirs(file_path, exist_ok=True)

    with open(temp_file_name, 'w') as f:
        f.write(response.text)


def remove_empty_folders(path, remove_root: bool = False):
    if not os.path.isdir(path):
        return

    # remove empty subfolders
    files = os.listdir(path)
    if len(files):
        for f in files:
            fullpath = os.path.join(path, f)
            if os.path.isdir(fullpath):
                remove_empty_folders(fullpath, remove_root=True)

    files = os.listdir(path)
    if len(files) == 0 and remove_root:
        os.rmdir(path)
