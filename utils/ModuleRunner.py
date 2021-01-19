import errno
import logging

from datetime import datetime
import os

from utils import Statics


class ModuleRunnerClass:

    def __init__(self):
        """ModuleRunnerClass this class runs each module 1 by 1 and when finished call the reporter..
                 Parameters:
                     :parameter None
                Returns:
                :returns None

                """

    def start_(self, input_imgs):
        """start_ this class runs each module 1 by 1 and when finished call the reporter..
                         Parameters:
                         :parameter input_imgs (dict): pass a dictionary containing img name and paths.
                         :parameter resultset (dict): pass a dictionary containing iimg info and real result in order to see the final report properly.
                         Returns:
                        :returns None

                        """
        Statics.LOGGER.logme("MODULE RUNNER starting to check for independent module dependencies ",
                             logging.INFO)
        for m in Statics.MODULES:
            if m.run == 1:
                Statics.LOGGER.logme("MODULE RUNNER running dependency check on  = " + str((m.return_my_dict())["name"]),
                                     logging.INFO)
                try:
                    m.check_deps()
                except Exception as e:
                    Statics.LOGGER.logme("MODULE RUNNER" + str(e),
                                         logging.CRITICAL)

        for m in Statics.MODULES:
            if m.run == 0:
                Statics.LOGGER.logme("MODULE RUNNER will not process = " + str(m.return_my_dict()["name"]),
                                     logging.INFO)
            else:


                Statics.LOGGER.logme(
                    "MODULE RUNNER Starting to process = " + str(m.return_my_dict()["name"]) + " for " + str(
                        len(input_imgs)),
                    logging.INFO)
                m.start_main_timer()
                m.prepare()

                for imgx in input_imgs:
                    m.prepare_img(input_imgs[imgx])
                    m.start_(input_imgs[imgx])
                m.end_main_timer()
