import os
import datetime
import zipfile

from syncomatic import app, lm
from syncomatic.models import User

def get_filelist(path):
    """
        Returns a list of dictionaries;
        Each dictionary contains the following keys:
        'name', 'size', 'creation_date', 'is_dir'
    """
    filenames = os.listdir(path)
    files = []
    for name in filenames:
        # os.stat returns a 10-tuple
        fullpath = os.path.join(path, name)
        stats = os.stat(fullpath)
        size = stats[6]
        creation_date = datetime.datetime.fromtimestamp(stats[-2]).strftime("%H:%M %d.%m.%Y")
        is_dir = os.path.isdir(fullpath)
        f = {'name': name, 'size': size, 'creation_date': creation_date,
            'is_dir': is_dir}
        files.append(f)

    return files

def get_unused_name(zipfolder):
    filename = 'files'
    ext = '.zip'
    if not os.path.exists(os.path.join(zipfolder, filename + ext)):
        return filename + ext
    else:
        i = 1
        while os.path.exists(os.path.join(zipfolder, filename + str(i) + ext)):
            i += 1

        return filename + str(i) + ext

def zipdir(path, zip_file):
    for root, folders, files in os.walk(path):
            # Include all subfolders, including empty ones.
            for folder_name in folders:
                # Item will be put inside archive under item_name
                item_name = os.path.join(os.path.basename(root), folder_name)
                zip_file.write(os.path.join(root, folder_name), item_name)

            for file_name in files:
                # Item will be put inside archive under item_name
                item_name = os.path.join(os.path.basename(root), file_name)
                zip_file.write(os.path.join(root, file_name), item_name)
