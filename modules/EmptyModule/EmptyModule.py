import subprocess

from utils import Statics
import itertools
import os
import platform
import lsb_release
from subprocess import STDOUT, check_call
from timeit import default_timer as timer

class EmptyModule:
    """
            This module is a reference point, if you wish add extra modules for reporting use this module as a base
            if you want this module to run change run=0 to run=1


        """
    prepare_start_time = None
    prepare_end_time = None
    start_time = None
    end_time = None
    each_img_process_time = {}
    run = 0
    using_gpu = 0
    my_info = {}
    model_usage = 0
    mymodels = []
    retrain = 0
    newlinux = 0

    def __init__(self, model_usage=0):

        self.model_usage = model_usage

        self.my_info["name"] = self.__class__
        self.my_info["using_gpu"] = self.using_gpu
        self.my_info["module_presentation"] = self.__doc__
        self.my_info["used models"] = self.mymodels

    def return_my_dict(self):
        return self.my_info

    def return_dict_with_results(self):
        return self.my_info

    def check_deps(self):
        pass

    def start_main_timer(self):
        start = timer()
        self.start_time = start

    def end_main_timer(self):
        end = timer()
        self.end_time = end

    def prepare_img(self, imgx):
        self.each_img_process_time[imgx] = {}
        start1 = timer()
        self.each_img_process_time[imgx]["prepare_start_"] = start1
        # process

        end1 = timer()
        self.each_img_process_time[imgx]["prepare_end"] = end1

    def prepare(self):
        start = timer()
        self.prepare_start_time = start

        end = timer()
        self.prepare_end_time = end

    def start_(self, imgx):
        start1 = timer()
        self.each_img_process_time[imgx]["_start"] = start1
        # process

        end1 = timer()
        self.each_img_process_time[imgx]["_end"] = end1
