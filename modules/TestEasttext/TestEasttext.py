import errno
import subprocess
import time

import cv2
import pytesseract
from PIL import Image

from utils import Statics
import itertools
import os
import platform
import lsb_release
from subprocess import STDOUT, check_call
from timeit import default_timer as timer
from imutils.object_detection import non_max_suppression
import numpy as np
from skimage.transform import resize,rescale

from utils.UtilsGeneric import image_resize, clear_text


class TestEasttext:
    """
                This Module uses East Text area detector..(as a frozen graph)
                in order to maximize the success ratio, i need at least 3000 pictures where the all checked by a HUMAN
                after that retraining will give you more than 95% success ratio.
                after finding text areas we will pass the areas to tesseract according tho top sizes..
                our main goal in this module to help tesseract work better by dropping usesless areas.


        """
    base_img=None
    prepared_img=None
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
    min_confidence=0.5
    default_width=320
    default_height=320
    rW = 0
    rH=0
    layerNames = [
        "feature_fusion/Conv_7/Sigmoid",
        "feature_fusion/concat_3"]
    net=None
    W=0
    H=0
    MY_RESULTS={}
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
        try:
            output_folder_name = 'INPUT_OUTPUT/outputs/' + str(self.__class__.__name__)
            os.makedirs(output_folder_name)
        except OSError as e:
            Statics.LOGGER.logme(str(self.__class__.__name__))+(str(e))

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
        self.MY_RESULTS[imgx]["prepare_start_"]  = start1
        # process
        self.base_img = cv2.imread(imgx)
        orig = self.base_img.copy()
        #image_resized = cv2.resize(orig,width=320,interpolation=cv2.INTER_CUBIC)
        image_resized=image = image_resize(orig, width = 320)
        (H, W) = image_resized.shape[:2]
        blank_image = np.zeros((self.default_width, self.default_height, 3), np.uint8)

        blank_image[:, :] = (255, 255, 255)
        blank_image[0: H, 0: W] = image_resized.copy()
        # set the new width and height and then determine the ratio in change
        # for both the width and height
        blank_image = cv2.fastNlMeansDenoisingColored(blank_image, None, 10, 10, 7, 21)
        #blank_image= cv2.adaptiveThreshold(blank_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
        img_gray = cv2.cvtColor(blank_image, cv2.COLOR_BGR2GRAY)
        img_blur = cv2.medianBlur(img_gray, 5)
        img_thresh_Gaussian = cv2.adaptiveThreshold(img_blur, 255,
                                                    cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        (thresh, blackAndWhiteImage) = cv2.threshold(img_thresh_Gaussian, 127, 255, cv2.THRESH_BINARY)

        #kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
        #self.prepared_img = cv2.filter2D(blank_image, -1, kernel)
        #self.prepared_img = cv2.cvtColor(self.prepared_img, cv2.COLOR_BGR2GRAY)

        fake_rgb = cv2.cvtColor(blackAndWhiteImage, cv2.COLOR_GRAY2RGB)
        copyx=fake_rgb.copy()
        fake_gray=cv2.cvtColor(copyx,cv2.COLOR_BGR2GRAY)
        contours, hier = cv2.findContours(fake_gray, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        blank_image2 = np.zeros((self.default_width, self.default_height, 3), np.uint8)

        blank_image2[:, :] = (255, 255, 255)
        # we are going to use a simple trick in there ...

        for cnt in contours:
            if 200 < cv2.contourArea(cnt) < 5000:
                cv2.drawContours(self.prepared_img, [cnt], 0, (0, 255, 0), 2)
                cv2.drawContours(self.prepared_img, [cnt], 0, 255, -1)
                cv2.drawContours(fake_gray, [cnt], 0, (0, 255, 0), 2)
                cv2.drawContours(fake_gray, [cnt], 0, 255, -1)
                x, y, w, h = cv2.boundingRect(cnt)
                ROI = fake_rgb[y:y + h, x:x + w]
                cloneimg=ROI.copy()
                blank_image2[y:y + h, x:x + w]=cloneimg
        cv2.imwrite("/tmp/" + str(round(time.time() * 1000)) + ".jpg",fake_rgb)
        cv2.imwrite("/tmp/aq_" + str(round(time.time() * 1000)) + ".jpg", fake_gray)
        cv2.imwrite("/tmp/blanker_" + str(round(time.time() * 1000)) + ".jpg", blank_image2)
        self.prepared_img = blank_image2
        (H, W) = blank_image.shape[:2]
        self.H=H
        self.W=W
        end1 = timer()
        self.each_img_process_time[imgx]["prepare_end_"] = end1
        self.MY_RESULTS[imgx]["prepare_end_"] = end1

    def prepare(self):
        start = timer()
        self.prepare_start_time = start
        self.MY_RESULTS["prepare_start"] = start
        pth=os.getcwd()+"/modules/"+str(self.__class__.__name__)+"/"+"frozen_east_text_detection.pb"

        self.net = cv2.dnn.readNet(pth)
        end = timer()
        self.prepare_end_time = end
        self.MY_RESULTS["prepare_end"] = end

    def start_(self, imgx):

        start1 = timer()
        self.each_img_process_time[imgx]["_start"] = start1
        self.MY_RESULTS[imgx]["_start"] = start1
        # process
        blob = cv2.dnn.blobFromImage(self.prepared_img, 1.0, (self.W, self.H),
                                     (123.68, 116.78, 103.94), swapRB=True, crop=False)
        self.net.setInput(blob)
        (scores, geometry) = self.net.forward(self.layerNames)
        (numRows, numCols) = scores.shape[2:4]

        rects = []
        confidences = []

        # loop over the number of rows, check probability and check also scores
        for y in range(0, numRows):

            scoresData = scores[0, 0, y]
            xData0 = geometry[0, 0, y]
            xData1 = geometry[0, 1, y]
            xData2 = geometry[0, 2, y]
            xData3 = geometry[0, 3, y]
            anglesData = geometry[0, 4, y]

            for x in range(0, numCols):
                # if our score does not have sufficient probability, ignore it
                if scoresData[x] < self.min_confidence:
                    continue
                # compute the offset factor as our resulting feature maps will
                # be 4x smaller than the input image
                (offsetX, offsetY) = (x * 4.0, y * 4.0)
                # extract the rotation angle for the prediction and then
                # compute the sin and cosine
                angle = anglesData[x]
                cos = np.cos(angle)
                sin = np.sin(angle)
                # use the geometry volume to derive the width and height of
                # the bounding box
                h = xData0[x] + xData2[x]
                w = xData1[x] + xData3[x]
                # compute both the starting and ending (x, y)-coordinates for
                # the text prediction bounding box
                endX = int(offsetX + (cos * xData1[x]) + (sin * xData2[x]))
                endY = int(offsetY - (sin * xData1[x]) + (cos * xData2[x]))
                startX = int(endX - w)
                startY = int(endY - h)
                # add the bounding box coordinates and probability score to
                # our respective lists
                rects.append((startX, startY, endX, endY))
                confidences.append(scoresData[x])
        boxes = non_max_suppression(np.array(rects), probs=confidences)
        # loop over the bounding boxes
        cp_img=self.prepared_img.copy()
        for (startX, startY, endX, endY) in boxes:
            # scale the bounding box coordinates based on the respective
            # ratios
            #startX = int(startX * self.rW)
            #startY = int(startY * self.rH)
            #endX = int(endX * self.rW)
            #endY = int(endY * self.rH)

            # extract the actual padded ROI
            roi = self.prepared_img[startY:endY, startX:endX]
            # draw the bounding box on the image
            cv2.rectangle(self.prepared_img, (startX, startY), (endX, endY), (0, 255, 0), 2)
        predicted_result = pytesseract.image_to_string(cp_img, lang='eng',
                                                       config='--oem 1 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')

        filter_predicted_result = "".join(predicted_result.split()).replace(":", "").replace("-", "").replace("_", "").replace(" ", "")
        cleared_text=clear_text(filter_predicted_result)
        self.MY_RESULTS[imgx]["result"]=cleared_text
        self.MY_RESULTS[imgx]["dirty_result"] = filter_predicted_result
        Statics.LOGGER.logme(str(self.__class__.__name__)+" => "+imgx + " -> " + filter_predicted_result)
        cv2.imwrite(imgx.replace('/img/',('/outputs/'+str(self.__class__.__name__))+"/") , self.prepared_img)
        end1 = timer()
        self.each_img_process_time[imgx]["_end"] = end1
        self.MY_RESULTS[imgx]["_end"] = end1