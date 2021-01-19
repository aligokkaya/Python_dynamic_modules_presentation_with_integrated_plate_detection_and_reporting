import os
import signal
from glob import glob
from utils import Statics
import logging
import json
from utils.Logger import LoggerClass
from utils.ModuleRunner import ModuleRunnerClass
from utils.Reporter import ReporterClass
from utils.UtilsGeneric import check_missing_python_packages, module_loader, input_img_searcher, zip_outputs_logs
import sys
import atexit
import shutil
def main():
    """Application starting point. Main function!
    It will check if you are root or not first, i only allow this code to work as root
    after that it will check system/packages.. , generate threads, and load modules dynamically.
    Everytime you add a new module you should restart this app to add it to process queu
         Parameters:
        :parameter None

        Returns:
        :returns None

        """
    directory_contents = os.listdir(Statics.OUTPUT_FOLDER)
    for d in directory_contents:

        if os.path.isdir(Statics.OUTPUT_FOLDER + d):
            shutil.rmtree(Statics.OUTPUT_FOLDER + d)
    # in order to backup logs and outputs for consecutive restarts of the test platform.. we will capture signal.. and run a function to copy logs outputs to a new folder, also zip the outcome to another folder for keeping longterm test results.
    signal.signal(signal.SIGTERM, lambda num, frame: sys.exit(0))
    # if there is missing packages , we will install automatically thats why we need root permission.. we
    # can install with -U setting but if we are running inside a docker its safe to not run  with a sudo
    if os.geteuid() != 0:
        exit("You need to have root privileges to run this script.\nPlease try again, this time using 'sudo'. Exiting.")
    Statics.LOGGER = LoggerClass()
    Statics.LOGGER.setup()
    Statics.LOGGER.logme(
        "This application developed with a Unix based system. if you dont have any missing packages it will work without your integration.\n")

    Statics.LOGGER.logme(
        "Checking system python packages, if anythng is missing you will be warned and this application will try to install it..\n")
    Statics.LOGGER.logme(
        "On some MacOs and Windows based systems installation will fail.. please install requirements with newly generated INPUT_OUTPUT/requirements.txt file\n")
    check_missing_python_packages()

    Statics.LOGGER.logme("Starting to process Models Folder to get all avaliable models.")
    module_loader(Statics.MODULE_PATH)
    Statics.LOGGER.logme("FOUND MODULES COUNT = "+str(len(Statics.MODULES)),logging.DEBUG)
    #initialize main module runner/controller
    Statics.MODULE_RUNNER=ModuleRunnerClass()
    #find all images in the Statics.INPUT_FOLDER
    Statics.LOGGER.logme("Searching for images recursively in "+Statics.INPUT_FOLDER, logging.INFO)
    input_imgs=input_img_searcher()
    Statics.LOGGER.logme("FOund "+str(len(input_imgs))+" images in" + Statics.INPUT_FOLDER, logging.INFO)

    Statics.LOGGER.logme("Found images" + json.dumps(input_imgs), logging.DEBUG)
    #process found images , pass RESULTSET too  in order to get full report
    Statics.LOGGER.logme("MODULE RUNNER STARTING FOR = "+str(len(Statics.MODULES))+" MODULES",logging.INFO)

    Statics.MODULE_RUNNER.start_(input_imgs)


def OnExitApp():
    Statics.REPORTER = ReporterClass()
    Statics.REPORTER.create_report()
    Statics.REPORTER.open_as_webpage()

    # first zip log and outputs to a secure place with timestamp...
    zip_outputs_logs(Statics.OUTPUT_FOLDER)
    # in order for next tests not to fail.. we should clear outputs folder..
    """directory_contents = os.listdir(Statics.OUTPUT_FOLDER)
    for d in directory_contents:

        if os.path.isdir(Statics.OUTPUT_FOLDER+d):
            shutil.rmtree(Statics.OUTPUT_FOLDER+d)
    """

if __name__ == '__main__':
    atexit.register(OnExitApp)
    main()


