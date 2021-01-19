import importlib
import os
import time
import zipfile
from datetime import datetime
from glob import glob

import cv2

from utils import Statics
from os import path
import logging
from zipfile import ZipFile
import os
from os.path import basename
import numpy as np
import re
from pathlib import Path
import zipfile
def input_img_searcher():
    """Search STATICS.INPUT_FOLDER for the extensions ('.jpg', '.png', '.jpeg', '.bmp', '.gif', '.tiff', '.webp')  recursively and create a dynamic dictionary
                Parameters:
                :parameter None
                Returns:
                :returns files_grabbed (dict): full list of file/folder of input imgs.

            """
    files_grabbed = {}
    for dirpath, dirs, files in os.walk(Statics.INPUT_FOLDER):
        for filename in files:
            fname = os.path.join(dirpath, filename)
            if fname.endswith(('.jpg', '.png', '.jpeg', '.bmp', '.gif', '.tiff', '.webp')):
                files_grabbed[filename]=fname
    Statics.FILES_GRABBED=files_grabbed
    return files_grabbed
def get_required_text(imgx):
    #print(Statics.INPUT_FOLDER+str(imgx))
    strx=Statics.INPUT_FOLDER+str(imgx)
    for m in Statics.RESULTSET:
        if m["img_name"] == strx :
            return m["real_result"]
def clear_text(str) :
    """clear non alphanumeric chars
                        Parameters:
                        :parameter str (string): string to be cleared
                        Returns:
                        :returns str (string) : cleared string

        """
    return re.sub(r'\W+', '', str)


def check_missing_python_packages():
    """Search given package list (Statics.PACKAGES) in the environment , if import fails it will try to install these packages
            Parameters:
            :parameter None
            Returns:
            :returns None

        """
    for package_name in Statics.PACKAGES:
        try:
            __import__(package_name)
            # import package_name
        except ImportError as error:
            Statics.LOGGER.logme(error.__class__.__name__ + ": " + str(error))
            Statics.LOGGER.logme("Trying to Install required module: " + package_name + "=>  " + Statics.PACKAGES[package_name][
                "compatible_name"] + "\n")
            os.system('pip3 install ' + Statics.PACKAGES[package_name]["compatible_name"])
        try:
            __import__(package_name)
            # import package_name
        except ImportError:
            # add this package to requirements file, i do not like to force any system with a ready to use requirements file
            # in most cases i compile my own tensorflow and opencv thats why if system has a precompiled versions of packages there is no need to force it to update/install
            write_requirements_file(Statics.PACKAGES[package_name])


def write_requirements_file(details):
    """Write requirements.txt file with missing system packages. Installation is straigtforward but on some systems it will fail to install.
    When this happens all dependency and requirements can be installed via
    "pip3 install -r INPUT_OUTPUT/requirements.txt"
    This file generated dynamically , if you have any package beforehand it will not add dependency on this file
    or it will not upgrade your versions.

         Parameters:
        :parameter  details (dict): Dictionary containing static module content from utils/Statics.py file
                        EXAMPLE :
                        "version":-1,
                        "compatible_name":"opencv-python"
        :returns None
     """
    # first check if there is a requirements txt file
    if path.exists(Statics.REQUIREMENTS_FILE):
        # read and search for your package
        package_found = 0
        with open(Statics.REQUIREMENTS_FILE) as search:
            for line in search:
                line = line.rstrip()  # remove '\n'
                if line.startswith(details["compatible_name"]):
                    package_found = 1
        if package_found == 0:
            with open(Statics.REQUIREMENTS_FILE, "a") as f:
                f.write("\n")
                if details["version"] == -1:
                    f.write(details["compatible_name"])
                else:
                    f.write(details["compatible_name"] + "==" + details["version"])
                f.close()
    else:
        f = open(Statics.REQUIREMENTS_FILE, "w")
        if details["version"] == -1:
            f.write(details["compatible_name"])
        else:
            f.write(details["compatible_name"] + "==" + details["version"])

        f.close()
def softmax( a):
    exps = np.exp(a.astype(np.float64))
    return exps / np.sum(exps, axis=-1)[:, np.newaxis]

def sigmoid( a):
    return 1. / (1. + np.exp(-a))
def image_resize(image, width = None, height = None, inter = cv2.INTER_NEAREST):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation = inter)

    # return the resized image
    return resized




def all_files(path):
    """iterator returns all files and folders from path as absolute path string
    """
    for child in Path(path).iterdir():
        yield str(child)
        if child.is_dir():
            for grand_child in all_files(str(child)):
                yield str(Path(grand_child))


def zip_dir(path):
    """generate a zip"""
    zip_filename = 'old_results/TEST_RESULTS_'+Statics.SESSION_STARTUP_TIME_STRING+'.zip'
    zip_file = zipfile.ZipFile(zip_filename, 'w')
    print('CREATED:', zip_filename)
    for file in all_files(path):
        print('adding... ', file)
        zip_file.write(file)
    zip_file.write(Statics.LOG_FILE_NAME, basename(Statics.LOG_FILE_NAME))
    for file in all_files(Statics.REPORT_PATH+Statics.REPORTER_DATETIME):
        print('adding... ', file)
        zip_file.write(file)


    zip_file.close()
def zip_outputs_logs(srcpath):
    """Search given directory recursively and generate a ZIP file with the timestamp

            Parameters:

            :parameter srcpath (string): directory to zip and move to old_results

            Returns:
            :returns None

        """
    try:
        os.makedirs('old_results/')
    except OSError as e:
        Statics.LOGGER.logme(str(e))
        zip_dir(srcpath,)






def module_loader(module_path):
    """Search given directory recursively and load modules

        Parameters:

        :parameter module_path (string): Base Modules folder to scan/search recursively [modules]

        Returns:
        :returns None

    """

    result = [y for x in os.walk(module_path) for y in glob(os.path.join(x[0], '*.py'))]
    Statics.LOGGER.logme(result)
    for str in result:
        str_class_name = os.path.basename(str)
        class_name = str_class_name.replace(".py", "")
        str_clean = str.replace(".py", "")

        module_name = str_clean.replace(os.sep, ".")
        # module_name = module_name[0:int(module_name.rfind('.'))]
        Statics.LOGGER.logme("MODULE_LOADER "+ " "+module_name+" "+class_name)


        module = importlib.import_module(module_name)
        class_ = getattr(module, class_name)
        instance = class_()

        Statics.MODULES.append(instance)
