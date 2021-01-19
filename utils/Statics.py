import logging
from utils.Logger import LoggerClass


"""Application generic settings and configuration files.
This file can be loaded from db/or conf file.. for this project single PY file approach is used.
:parameter PACKAGES (dict) : holds reuired packages and their required version, if version number is -1 it will install the latest. and version number will not put in requirements.txt
:parameter REQUIREMENTS_FILE (string): holds the place where we should write requirements file.
:parameter MODULES (array of classes): hold dynamically found modules inside the modules folder. it will initialize and hold the classes
:parameter MODULE_PATH (string): holds the modules directory where we will search modules automatically
:parameter CONSOLE_LOGGER_LEVEL (int): holds loggers logging.INFO/DEBUG.. integer values for console logging level
:parameter FILE_LOGGER_LEVEL (int): holds loggers logging.INFO/DEBUG.. integer values for file logging level
:parameter LOG_FILE_NAME (string): base log file name, datetime will be added automatically in the begining of this filename. ".log" will be added automatically in the end.
:parameter LOG_FOLDER (string): log folder to save log files.
:parameter LOGGER  (LoggerClass): did not want to use singleton object pattern just hold a logger in this file and call it from all over the code.
:parameter RESULTSET (dict) : results and img names in order to calculate final success ratio. if imgs are changed you should change this resultset too in order to see a proper test result paper.
:parameter MODULE_RUNNER (ModuleRunnerClass) : main module controller class
:parameter OUTPUT_FOLDER (string) : directory location to place output report
:parameter INPUT_FOLDER (string) : directory location to search recursively for images
:parameter SESSION_STARTUP_TIME_STRING (string) : session startup time as string in order to match outputs and logs
:parameter LOG_FILE_NAME (string) : session log file name
:parameter REPORT_PATH (string) : final report directory 
:parameter REPORTER (ReporterClass) : reference to report creation class
        """
SESSION_STARTUP_TIME_STRING=None
LOG_FILE_NAME=None
PACKAGES = {
    "cv2": {
        "version": -1,
        "compatible_name": "opencv-python"
    },
    "tensorflow": {
        "version": "2.4.0",
        "compatible_name": "tensorflow"
    },
    "beautifultable": {
        "version": -1,
        "compatible_name": "beautifultable"
    },
    "fpdf": {
        "version": -1,
        "compatible_name": "fpdf"
    },
    "testresources": {
        "version": -1,
        "compatible_name": "testresources"
    },
    "PIL": {
        "version": -1,
        "compatible_name": "pillow"
    },
    "pytesseract": {
        "version": -1,
        "compatible_name": "pytesseract"
    },
    "imutils": {
        "version": -1,
        "compatible_name": "imutils"
    },
    "openalpr":{
        "version": -1,
        "compatible_name": "openalpr"
    }
    ,"skimage":{
        "version": -1,
        "compatible_name": "scikit-image"
    }
,"lxml":{
        "version": -1,
        "compatible_name": "lxml"
    }
,"absl":{
        "version": -1,
        "compatible_name": "absl-py"
    }
,"tqdm":{
        "version": -1,
        "compatible_name": "tqdm"
    }
,"easydict":{
        "version": -1,
        "compatible_name": "easydict"
    }
,"matplotlib":{
        "version": -1,
        "compatible_name": "matplotlib"
    }
    ,"editdistance":{
        "version":-1,
        "compatible_name":"editdistance"

    }
,"pyclipper":{
        "version":-1,
        "compatible_name":"pyclipper"
    }
    ,"h5py":{
        "version":-1,
        "compatible_name":"h5py"
    },
    "pandas":{
        "version":-1,
        "compatible_name":"pandas"
    },
    "scipy":{
        "version":-1,
        "compatible_name":"scipy"
    }
    ,"nms":{
        "version":-1,
        "compatible_name":"nms"
    }
    ,"shapely":{
        "version":-1,
        "compatible_name":"shapely"
    }
,"xlsxwriter":{
        "version":-1,
        "compatible_name":"xlsxwriter"
    }
,"mxnet":{
        "version":-1,
        "compatible_name":"mxnet"
    }
,"torch":{
        "version":"1.6.0+cpu",
        "compatible_name":"torch"
    }
,"torchvision":{
        "version":"0.7.0+cpu",
        "compatible_name":"torchvision"
    }
,"gluoncv":{
        "version":-1,
        "compatible_name":"gluoncv"
    }

,"yaml":{
        "version":-1,
        "compatible_name":"pyyaml"
    }
,"rospkg":{
        "version":-1,
        "compatible_name":"rospkg"
    }

,"sympy":{
        "version":-1,
        "compatible_name":"sympy"
    }
    ,"fuzzywuzzy":{
        "version":-1,
        "compatible_name":"fuzzywuzzy"
    }


}
REQUIREMENTS_FILE = "INPUT_OUTPUT/requirements.txt"
FILES_GRABBED= None
MODULES = []
MODULE_PATH = "modules"
REPORT_PATH = "INPUT_OUTPUT/reports/"
REPORTER=None
CONSOLE_LOGGER_LEVEL = logging.DEBUG
FILE_LOGGER_LEVEL = logging.DEBUG
LOG_FILE_NAME = "LOG_OUTPUT"
LOG_FOLDER = "logs"
REPORTER_DATETIME=None
LOGGER = None
MODULE_RUNNER = None
OUTPUT_FOLDER="INPUT_OUTPUT/outputs/"
INPUT_FOLDER="INPUT_OUTPUT/img/"
# model results section will be filled on the runtiime by each module..
RESULTSET = [
    {
        "img_name" : "INPUT_OUTPUT/img/0x0-2.jpg",
        "real_result" : "34DUA34"

    }
    ,
    {
        "img_name": "INPUT_OUTPUT/img/5DYvgL.jpg",
        "real_result": "34ZB3636"

    }
    ,
    {
        "img_name": "INPUT_OUTPUT/img/44_ab_044_malatya_ozel_plaka_sat_l_k_8390135523727512913.jpg",
        "real_result": "44AB044"

    }
,
    {
        "img_name": "INPUT_OUTPUT/img/61BB2F3F8DE7424F88551964D7D0252F.jpg",
        "real_result": "35AP7605"

    }
,
    {
        "img_name": "INPUT_OUTPUT/img/440px-Turkey_licenceplate.jpg",
        "real_result": "38VU055"

    }
,
    {
        "img_name": "INPUT_OUTPUT/img/app-plakalar-cesitleri-129120064433690-12.jpeg",
        "real_result": "06KB848"


    }
,
    {
        "img_name": "INPUT_OUTPUT/img/app-plakalar-cesitleri-129120064433690-1223.jpeg",
        "real_result": "06AY6651"

    }
,
    {
        "img_name": "INPUT_OUTPUT/img/bos-plaka-bulma.jpg",
        "real_result": "06GKN62"

    }
,
    {
        "img_name": "INPUT_OUTPUT/img/download223.jpg",
        "real_result": "35AD7227"

    }
,
    {
        "img_name": "INPUT_OUTPUT/img/download33221.jpg",
        "real_result": "42FNG29"

    }
,
    {
        "img_name": "INPUT_OUTPUT/img/images.jpg",
        "real_result": "19AAB001"

    }

,
    {
        "img_name": "INPUT_OUTPUT/img/images (2).jpg",
        "real_result": "06LRN01"

    }
,
    {
        "img_name": "INPUT_OUTPUT/img/images (3).jpg",
        "real_result": "09BT449"

    }
,
    {
        "img_name": "INPUT_OUTPUT/img/plaka-png-1.png",
        "real_result": "06CNU56"

    }
,
    {
        "img_name": "INPUT_OUTPUT/img/rckdr5Tfmka3XzHlJJU0JA222.jpg",
        "real_result": "34VG743"

    }
,
    {
        "img_name": "INPUT_OUTPUT/img/tr-plaka-png-4.png",
        "real_result": "34SG1957"

    }
,
    {
        "img_name": "INPUT_OUTPUT/img/turk35GA4434.jpg",
        "real_result": "35GS4434"

    }
,
    {
        "img_name": "INPUT_OUTPUT/img/turkije23.jpg",
        "real_result": "35AD4597"

    }
,
    {
        "img_name": "INPUT_OUTPUT/img/turkije36.jpg",
        "real_result": "03HP408"

    }

,
    {
        "img_name": "INPUT_OUTPUT/img/unnamed (1).jpg",
        "real_result": "33BJJ09"

    }


]

