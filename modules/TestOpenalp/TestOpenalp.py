import subprocess

from openalpr import Alpr

from utils import Statics
import itertools
import os
import platform
import lsb_release
from subprocess import STDOUT, check_call
from timeit import default_timer as timer
import ctypes
import json
import re
from utils.UtilsGeneric import clear_text

unicode = str
_PYTHON_3 = True
def _convert_to_charp(string):
    # Prepares function input for use in c-functions as char*
    if type(string) == unicode:
        return string.encode("UTF-8")
    elif type(string) == bytes:
        return string
    else:
        raise TypeError("Expected unicode string values or ascii/bytes values. Got: %r" % type(string))

def _convert_from_charp(charp):
    # Prepares char* output from c-functions into Python strings
    if _PYTHON_3 and type(charp) == bytes:
        return charp.decode("UTF-8")
    else:
        return charp
class TestOpenalp:
    """
            ATTENTION !! THIS MODULE ONLY WORKS ON DEBIAN BASED SYSTEMS
            sudo apt-get install -y openalpr openalpr-daemon openalpr-utils libopenalpr-dev

            If you wish to run this code on a raspberry or arm systems.. you should COMPILE !!

            This Module uses Open ALP success rate is so so...


        """
    prepare_start_time = None
    prepare_end_time = None
    start_time = None
    end_time = None
    each_img_process_time = {}
    run=1
    using_gpu = 0
    my_info = {}
    model_usage = 0
    mymodels = []
    retrain = 0
    newlinux=0
    region="eu"
    conf = "/etc/openalpr/openalpr.conf"
    runtime = "/usr/share/openalpr/runtime_data/"
    alpr = None
    HOW_MANY_PASSES = 10
    MY_RESULTS ={}

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

        # first check if alpr is installed..
        install_me=0
        return_data = ""
        try:
            result = subprocess.run(['alpr', '-v'], stdout=subprocess.PIPE)
            return_data = result.stdout
        except :
            install_me=1

        if return_data.find("not found") > -1  or install_me == 1:
            # openalpr is not installed
            check_call(['apt-get', 'install', '-y', 'openalpr', 'openalpr-daemon', 'openalpr-utils', 'libopenalpr-dev'],
                       stdout=open(os.devnull, 'wb'), stderr=STDOUT)
        try:
            output_folder_name = 'INPUT_OUTPUT/outputs/' + str(self.__class__.__name__)
            os.makedirs(output_folder_name)
        except OSError as e:
            Statics.LOGGER.logme(str(self.__class__.__name__)+" "+str(e))

    def start_main_timer(self):
        start = timer()
        self.start_time = start
        self.MY_RESULTS["main_timer_start"] = start

    def end_main_timer(self):
        end = timer()
        self.end_time = end
        self.MY_RESULTS["main_timer_end"] = end

    def prepare_img(self, imgx):
        self.each_img_process_time[imgx] = {}
        self.MY_RESULTS[imgx] = {}
        start1 = timer()
        self.each_img_process_time[imgx]["prepare_start_"] = start1
        self.MY_RESULTS[imgx]["prepare_start_"] = start1
        # process
        # no preparing needed
        end1 = timer()
        self.each_img_process_time[imgx]["prepare_end"] = end1
        self.MY_RESULTS[imgx]["prepare_end_"] = end1

    def prepare(self):
        start = timer()
        self.prepare_start_time = start
        # no prepare needed
        self.MY_RESULTS["prepare_start"] = start

        end = timer()
        self.prepare_end_time = end
        self.MY_RESULTS["prepare_end"] = end

    def start_(self, imgx):

        start1 = timer()
        self.each_img_process_time[imgx]["_start"] = start1
        self.MY_RESULTS[imgx]["_start"] = start1
        # process
        img_path=os.getcwd()+"/"+imgx
        result = subprocess.run(['alpr', '-c',"eu" , img_path], stdout=subprocess.PIPE)
        return_data = result.stdout.decode('utf-8')
        i = 0

        parse_str=str(return_data).split("\n")
        resultset={}
        count = 0
        for s in parse_str:
            if s.find("confidence") > -1:
                #news=clear_text(s)
                foostr=re.split(r'\t+', s)
                if len(foostr)>=1 :
                    plate=clear_text(foostr[0])
                    clear_percentage=foostr[1].replace(" confidence: ","")
                    clear_percentage =float(clear_percentage)
                    foo_result={"plate":plate,"percentage":clear_percentage}
                    resultset[count]=foo_result
                    count = count+1


                Statics.LOGGER.logme(str(self.__class__.__name__) + " " + str(foostr))


        biggest_percentage=float(0)
        plate_of_biggest_percentage=""
        for i in resultset :
            mydata=resultset[i]
            if mydata["percentage"] > biggest_percentage :
                biggest_percentage=mydata["percentage"]
                plate_of_biggest_percentage =mydata["plate"]
        self.MY_RESULTS[imgx]["result"] = plate_of_biggest_percentage
        self.MY_RESULTS[imgx]["dirty_result"] = clear_text(plate_of_biggest_percentage)




        end1 = timer()
        self.each_img_process_time[imgx]["_end"] = end1
        self.MY_RESULTS[imgx]["_end"] = end1

    def end_(self):
        self.alpr.unload()
