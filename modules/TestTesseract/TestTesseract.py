import subprocess
import time

from utils import Statics
import itertools
import os
import platform
import lsb_release
from subprocess import STDOUT, check_call
from timeit import default_timer as timer
import cv2
import pytesseract
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image as im
from scipy.ndimage import interpolation as inter
import re
import string

from utils.UtilsGeneric import image_resize, clear_text


class TestTesseract:
    """
            ATTENTION !! THIS MODULE ONLY WORKS ON DEBIAN BASED SYSTEMS
            sudo add-apt-repository ppa:alex-p/tesseract-ocr
            sudo apt-get update
            sudo apt install tesseract-ocr

            If you wish to run this code on a raspberry or arm systems.. you should COMPILE !!

            This Module uses base tesseract methods to determine texts on a image..
            Tesseract is around for a very long period of time..
            we even manage to convert HANDWRITTEN OTTOMAN Language to digital texts.
            Unfortunately this module REQUIRES PROPER dataset and training..
            as long as you have a clean dataset you will get min %95 success ratio.
            for plate recognition this model is too expensive..
            but the idea about it is the same if you have a very competitive company against you..
            this should be the way you follow to showoff the difference in engineering  quality..


        """
    pytesseract.pytesseract.tesseract_cmd = 'tesseract'
    base_img=None
    prepared_img=None
    prepare_start_time=None
    prepare_end_time=None
    start_time=None
    end_time=None
    each_img_process_time= {}

    run =1
    using_gpu = 0
    my_info = {}
    model_usage = 0
    mymodels = []
    retrain = 0
    newlinux=0

    min_confidence = 0.5
    default_width = 320
    default_height = 320
    rW = 0
    rH = 0
    MY_RESULTS = {}
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
        # first check version of linux.
        str = lsb_release.get_lsb_information()
        release=str["RELEASE"]
        if release.startswith("18") or release.starsWith("19") or release.startsWith("20"):
            self.newlinux=1
        # first check if tesseract is installed..
        return_data=""
        try_to_install=0
        try :
            result = subprocess.run(['tesseract', '-v'], stdout=subprocess.PIPE)
            return_data=result.stdout
            if return_data.find("not found") > -1 or return_data.find("No such file or directory") > -1 :
                try_to_install=1
        except:
            try_to_install=1

        if try_to_install == 1 :
            # tesseract is not installed
            if self.newlinux == 1:
                # can install with apt-get
                check_call(['apt-get', 'install', '-y', 'tesseract-ocr'],
                           stdout=open(os.devnull, 'wb'), stderr=STDOUT)
            else :
                check_call([ 'add-apt-repository',  '-y', 'ppa:alex-p/tesseract-ocr'],
                           stdout=open(os.devnull, 'wb'), stderr=STDOUT)
                check_call([ 'apt-get', 'update'],
                           stdout=open(os.devnull, 'wb'), stderr=STDOUT)
                check_call([ 'apt-get', 'install', '-y', 'tesseract-ocr'],
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
        img = cv2.imread(imgx)
        self.base_img = cv2.imread(imgx)
        orig = self.base_img.copy()
        # image_resized = cv2.resize(orig,width=320,interpolation=cv2.INTER_CUBIC)
        image_resized =  image_resize(orig, width=320)
        (H, W) = image_resized.shape[:2]

        # set the new width and height and then determine the ratio in change
        # for both the width and height
        blank_image = cv2.fastNlMeansDenoisingColored(image_resized, None, 10, 10, 7, 21)
        # blank_image= cv2.adaptiveThreshold(blank_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
        img_gray = cv2.cvtColor(blank_image, cv2.COLOR_BGR2GRAY)
        img_blur = cv2.medianBlur(img_gray, 5)
        img_thresh_Gaussian = cv2.adaptiveThreshold(img_blur, 255,
                                                    cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        (thresh, blackAndWhiteImage) = cv2.threshold(img_thresh_Gaussian, 127, 255, cv2.THRESH_BINARY)

        # kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
        # self.prepared_img = cv2.filter2D(blank_image, -1, kernel)
        # self.prepared_img = cv2.cvtColor(self.prepared_img, cv2.COLOR_BGR2GRAY)

        fake_rgb = cv2.cvtColor(blackAndWhiteImage, cv2.COLOR_GRAY2RGB)
        copyx = fake_rgb.copy()
        fake_gray = cv2.cvtColor(copyx, cv2.COLOR_BGR2GRAY)
        contours, hier = cv2.findContours(fake_gray, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        blank_image2 = np.zeros((H, W, 3), np.uint8)

        blank_image2[:, :] = (255, 255, 255)
        blank_image3 = np.zeros((H, W, 3), np.uint8)

        blank_image3[:, :] = (255, 255, 255)
        # we are going to use a simple trick in there ...
        # if we know the font then it will be alot easier to calculate and get the contour according to font aspect ratio..
        # but it is a little messy..
        # so.. LETS take a ratio where our value is the overall ratio of common fonts..
        """Arial 	0.52
            Avant Garde 	0.45
            Bookman 	0.40
            Calibri 	0.47
            Century Schoolbook 	0.48
            Cochin 	0.41
            Comic Sans 	0.53
            Courier 	0.43
            Courier New 	0.42
            Garamond 	0.38
            Georgia 	0.48
            Helvetica 	0.52
            Palatino 	0.42
            Tahoma 	0.55
            Times New Roman 	0.45
            Trebuchet 	0.52
            Verdana 	0.58
            ------------------------------------
            W is messing with the calculations.. but wahtsoever.. their average is 0.471176470588235
            so it is 0,472
            but we are not looking all plates with birds eye.. and some of them are really messy..
             
            lets assume we are alooking with 45 degree.. (simple opengl calculations..) i m not forcing these calculations
            to be taken with all possible scenarios.. i m just calculating for 2 scenarios where width and height alone can change alot.. 
            then our 0.472 can become -> w=472 h=1000 
                                            => rectangular area Height will increase 1000+472÷√2=1333,75
                                            => rectangular area WIDTH will drop to 472÷√2=333.75
                                            => so our 0.472 will become 0.25
            lets assume we are looking from a higher place where Height will look smaller.. lets assume again 45 degrees
                                        -> w=472  h=1000
                                            => this time width will stay same..   472
                                            => heigh will change Angle ∠A = 22.5° = 22°30'0" = 0.3927 rad = π/8
                                                                Angle ∠B = 22.5° = 22°30'0" = 0.3927 rad = π/8
                                                                Angle ∠C = 135° = 2.35619 rad = 3/4π 
                                                                Side a = 541.1961
                                                                Side b = 541.1961
                                                                Side c = 1,000
                                                                
                                                                So our 0.472 will become to 472/541.19 =0.872
            so we will use 0.25 to 0.872
            -> we should consider 1 more thing. first countours are not perfect because whatever we do to increase image quality there will be always nested contours
            or multiple chars to be accepted as one.. 
            so => first get image width into consideration.. with maximum minimum char count.. and find a proper orientation between them and newly calculated averages
            
            
            
            
            height/wiodth ratio
    ATTENTION !! this paart should be calculated with lots of samples.. in order to see perfect ratio
            
        
        """

        for cnt in contours:
            if 200 < cv2.contourArea(cnt) < 5000:
                cv2.drawContours(self.prepared_img, [cnt], 0, (0, 255, 0), 2)
                cv2.drawContours(self.prepared_img, [cnt], 0, 255, -1)
                cv2.drawContours(fake_gray, [cnt], 0, (0, 255, 0), 2)
                cv2.drawContours(fake_gray, [cnt], 0, 255, -1)
                x, y, w, h = cv2.boundingRect(cnt)
                ROI = fake_rgb[y:y + h, x:x + w]
                cloneimg = ROI.copy()
                blank_image2[y:y + h, x:x + w] = cloneimg
        average_min=0.25
        average_max=0.872

        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            average = w/h


            if average_min <= average <= average_max :
                ROI = fake_rgb[y:y + h, x:x + w]
                cloneimg = ROI.copy()
                blank_image3[y:y + h, x:x + w] = cloneimg

        cv2.imwrite("/tmp/blank_image3" + str(round(time.time() * 1000)) + ".jpg", blank_image3)
        cv2.imwrite("/tmp/blank_image2" + str(round(time.time() * 1000)) + ".jpg", blank_image2)
        self.prepared_img = blank_image3

        self.base_img = img

        end1 = timer()
        self.each_img_process_time[imgx]["prepare_end_"] = end1
        self.MY_RESULTS[imgx]["prepare_end_"] = end1
    def prepareold_img(self,imgx):
        self.each_img_process_time[imgx] = {}
        start1 = timer()
        self.each_img_process_time[imgx]["prepare_start_"]=start1
        # process
        img = cv2.imread(imgx)

        #now try to resize ... remove noise...
        resize_test_license_plate = cv2.resize(
            img, None, fx=2, fy=2,
            interpolation=cv2.INTER_CUBIC)

        grayscale_resize_test_license_plate = cv2.cvtColor(
            resize_test_license_plate, cv2.COLOR_BGR2GRAY)

        gaussian_blur_license_plate = cv2.GaussianBlur(
            grayscale_resize_test_license_plate, (5, 5), 0)
        ret, imgf = cv2.threshold(gaussian_blur_license_plate, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        gray = cv2.medianBlur(imgf, 3)
        imgf = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)


        self.prepared_img = imgf
        self.base_img=img

        end1 = timer()
        self.each_img_process_time[imgx]["prepare_end"] =end1

    def prepare(self):
        start = timer()
        self.prepare_start_time = start
        self.MY_RESULTS["prepare_start"] = start

        end = timer()
        self.prepare_end_time = end
        self.MY_RESULTS["prepare_end"] = end

    def start_(self, imgx):
        start1 = timer()
        self.each_img_process_time[imgx]["_start"] = start1
        self.MY_RESULTS[imgx]["_start"] = start1
        # process
        base2 = self.base_img.copy()
        hsv = cv2.cvtColor(base2, cv2.COLOR_BGR2HSV)
        lower = np.array(np.array([0,0,0], dtype=np.uint8), dtype="uint8")
        upper = np.array(np.array([0,0,255], dtype=np.uint8), dtype="uint8")

        # find the colors within the specified boundaries and apply
        # the mask
        mask = cv2.inRange(hsv, lower, upper)
        output = cv2.bitwise_and(base2, base2, mask=mask)

        ret, thresh = cv2.threshold(mask, 40, 255, 0)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        if len(contours) != 0:
            # draw in blue the contours that were founded
            cv2.drawContours(output, contours, -1, 255, 3)

            # find the biggest countour (c) by the area
            c = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(c)

            # draw the biggest contour (c) in green
            cv2.rectangle(output, (x, y), (x + w, y + h), (0, 255, 0), 2)

        #cv2.imwrite(imgx.replace('/img/',('/outputs/'+str(self.my_info["name"]))+"/"),output)
        predicted_result = pytesseract.image_to_string(self.prepared_img, lang='eng',
                                                       config='--oem 1 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')

        filter_predicted_result = "".join(predicted_result.split()).replace(":", "").replace("-", "").replace("_", "").replace(" ", "")
        cleared_text = clear_text(filter_predicted_result)
        self.MY_RESULTS[imgx]["result"] = cleared_text
        self.MY_RESULTS[imgx]["dirty_result"] = filter_predicted_result

        #print(imgx + " -> " + pytesseract.image_to_string(self.prepared_img))
        cv2.imwrite(imgx.replace('/img/', ('/outputs/' + str(self.my_info["name"])) + "/"), output)
        Statics.LOGGER.logme(str(self.__class__.__name__)+" "+imgx+ " -> "+filter_predicted_result)

        end1 = timer()
        self.each_img_process_time[imgx]["_end"] = end1
        self.MY_RESULTS[imgx]["_end"] = end1



    def find_score(self, arr, angle):
        data = inter.rotate(arr, angle, reshape=False, order=0)
        hist = np.sum(data, axis=1)
        score = np.sum((hist[1:] - hist[:-1]) ** 2)
        return hist,  1