import logging

from datetime import datetime
import os

from utils import Statics


class LoggerClass:

    def __init__(self):
        """LoggerClass this class generates handlers for logging and defines the configuration..
                 Parameters:
                :parameter None
                Returns:
                :returns None

                """

        # check if folder exists
        if not os.path.exists(Statics.LOG_FOLDER):
            try:
                os.mkdir(Statics.LOG_FOLDER)
            except OSError:
                print("Creation of the directory %s failed" % Statics.LOG_FOLDER)
        else:
            print("Log Folder Exists Starting Logger %s " % Statics.LOG_FOLDER)
        print("STARTING LOGGER !!!!!!\n\n\n")
        # create console logger

        self.logme("LOGGER STARTED !!\n", logging.INFO)
    def setup(self):
        logger = logging.getLogger("dev")
        logger.setLevel(logging.DEBUG)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(Statics.CONSOLE_LOGGER_LEVEL)
        c_format = logging.Formatter('%(asctime)s  %(name)s  %(levelname)s: %(message)s')
        console_handler.setFormatter(c_format)
        # append console handler to logger
        logger.addHandler(console_handler)
        # fill filename with datetime
        now = datetime.now()
        dt_string = now.strftime("%d_%m_%Y__%H_%M_%S")
        Statics.SESSION_STARTUP_TIME_STRING=dt_string
        filename = Statics.LOG_FOLDER + os.path.sep + dt_string + "___" + Statics.LOG_FILE_NAME + ".log"
        Statics.LOG_FILE_NAME=filename
        print("New Log file name is => " +filename+"\n" )

        # create file logger
        file_handler = logging.FileHandler(filename)
        file_handler.setLevel(Statics.FILE_LOGGER_LEVEL)
        f_format = logging.Formatter('%(asctime)s  %(name)s  %(levelname)s: %(message)s')
        file_handler.setFormatter(f_format)

        # append file handler to logger
        logger.addHandler(file_handler)
    def logme(self, str, level=logging.INFO):
        """Log helper class, in order to take full control and not to use static functions.
         Parameters:
        :parameter str (string): log text
        :parameter level (int): logging.INFO/logging.DEBUG ... should be passed
        Returns:
        :returns None

        """
        logger = logging.getLogger("dev")
        if level == logging.DEBUG:
            logger.debug(str)
        elif level == logging.INFO:
            logger.info(str)
        elif level == logging.WARNING:
            logger.warning(str)
        elif level == logging.ERROR:
            logger.error(str)
        elif level == logging.CRITICAL:
            logger.critical(str)
        else:
            logger.info(str)

