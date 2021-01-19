import errno
import logging

from datetime import datetime
import os

from beautifultable import BeautifulTable

from utils import Statics
from difflib import SequenceMatcher
import numpy as np
from fuzzywuzzy import fuzz

from utils.UtilsGeneric import get_required_text
import xlsxwriter

class ReporterClass:

    def __init__(self):
        """ReporterClass this class generates reports for all modules.. and create their comparison tables..
                 Parameters:
                :parameter None
                Returns:
                :returns None

                """

        # check if folder exists
        if not os.path.exists(Statics.REPORT_PATH):
            try:
                os.mkdir(Statics.REPORT_PATH)
            except OSError:
                Statics.LOGGER.logme(
                    str(self.__class__.__name__) + " " + "Creation of the directory %s failed" % Statics.LOG_FOLDER)

    def similar(self, a, b):
        """calculate similarity between 2 texts
                         Parameters:
                        :parameter a (string): first text to check similarity
                        :parameter b (string): second text to check similarity
                        Returns:
                        :returns int : 0-1 similarity ratio..

                        """
        Str1 = "The supreme court case of Nixon vs The United States"
        Str2 = "Nixon v. United States"
        Ratio = fuzz.ratio(Str1.lower(), Str2.lower())
        Partial_Ratio = fuzz.partial_ratio(Str1.lower(), Str2.lower())
        Token_Sort_Ratio = fuzz.token_sort_ratio(Str1, Str2)
        Token_Set_Ratio = fuzz.token_set_ratio(Str1, Str2)

        # return SequenceMatcher(None, a, b).ratio()
        return (Ratio, Partial_Ratio, Token_Sort_Ratio, Token_Set_Ratio)

    def filecreation(self,tablex, filename,timex):
        mydir = os.getcwd()+"/INPUT_OUTPUT/reports/"+timex+"/"
        try:
            os.makedirs(mydir)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise  # This was not a "directory exist" error..
        with open(os.path.join(mydir, filename), 'w') as d:
            d.write(tablex.__str__())
    def create_report(self):
        # first step is creating multiple tables to see the result
        timex=datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        Statics.REPORTER_DATETIME=datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        workbook = xlsxwriter.Workbook(os.getcwd()+"/INPUT_OUTPUT/reports/"+timex+"/ALL_REPORTS_AS_EXCEL.xlsx")
        worksheets = {}
        cell_format = workbook.add_format()
        cell_format.set_bold()

        for m in Statics.MODULES:
            if m.run ==1:
                worksheet_name =str(m.__class__.__name__)
                worksheets[worksheet_name] = workbook.add_worksheet(worksheet_name)
                #write excel header
                count =0
                for s in ["Module Name", "Process", "start time", "end_time", "delta_time_seconds"]:
                    worksheets[worksheet_name].write(0, count, s, cell_format)
                    count = count + 1

                myfoo = 1
                count = 0
                for s in [str(m.__class__.__name__), "Total ", m.MY_RESULTS["main_timer_start"],
                     m.MY_RESULTS["main_timer_end"],
                     (m.MY_RESULTS["main_timer_end"] - m.MY_RESULTS["main_timer_start"])]:
                    # print(i)

                    worksheets[worksheet_name].write(myfoo, count, s)
                    count = count + 1

                count = 0
                myfoo = myfoo + 1
                for s in [str(m.__class__.__name__), "Prep Work", m.MY_RESULTS["prepare_start"],
                                   m.MY_RESULTS["prepare_end"],
                                   (m.MY_RESULTS["prepare_end"] - m.MY_RESULTS["prepare_start"])]:

                    worksheets[worksheet_name].write(myfoo, count, s)

                    count = count +1


                table = BeautifulTable(maxwidth=200)
                table.columns.header = ["Module Name", "Process", "start time", "end_time", "delta_time_seconds"]



                table.rows.append(
                    [str(m.__class__.__name__), "Total ", m.MY_RESULTS["main_timer_start"],
                     m.MY_RESULTS["main_timer_end"],
                     (m.MY_RESULTS["main_timer_end"] - m.MY_RESULTS["main_timer_start"])])
                table.rows.append([str(m.__class__.__name__), "Prep Work", m.MY_RESULTS["prepare_start"],
                                   m.MY_RESULTS["prepare_end"],
                                   (m.MY_RESULTS["prepare_end"] - m.MY_RESULTS["prepare_start"])])
                Statics.LOGGER.logme(
                    "--------------------------------------------------------------------------------------")

                for imgx in Statics.FILES_GRABBED:
                    mydat = Statics.INPUT_FOLDER + imgx

                    table.rows.append([str(imgx), "img Prep", m.MY_RESULTS[mydat]["prepare_start_"],
                                       m.MY_RESULTS[mydat]["prepare_end_"],
                                       (m.MY_RESULTS[mydat]["prepare_end_"] - m.MY_RESULTS[mydat]["prepare_start_"])])

                    table.rows.append([str(imgx), "img process", m.MY_RESULTS[mydat]["_start"],
                                       m.MY_RESULTS[mydat]["_end"],
                                       (m.MY_RESULTS[mydat]["_end"] - m.MY_RESULTS[mydat]["_start"])])
                Statics.LOGGER.logme(table)
                self.filecreation(table,str(m.__class__.__name__)+timex+".txt",timex)
                table2 = BeautifulTable(maxwidth=200)

                table2.columns.header = ["Img Name", "Required_text", "Found Text", "FoundText Ratio",
                                         "FoundText Partial_Ratio", "FoundText Token_Sort_Ratio",
                                         "FoundText Token_Set_Ratio",
                                         "Dirty Text", "Dirty Text Ratio", "Dirty Text Partial_Ratio",
                                         "Dirty Text Token_Sort_Ratio", "Dirty Text Token_Set_Ratio"]
                worksheet_name=str(m.__class__.__name__)+"_RESULT_DETAILS_"
                worksheets[worksheet_name] = workbook.add_worksheet(
                    worksheet_name)
                # write excel header
                count = 0
                for s in  ["Img Name", "Required_text", "Found Text", "FoundText Ratio",
                                         "FoundText Partial_Ratio", "FoundText Token_Sort_Ratio",
                                         "FoundText Token_Set_Ratio",
                                         "Dirty Text", "Dirty Text Ratio", "Dirty Text Partial_Ratio",
                                         "Dirty Text Token_Sort_Ratio", "Dirty Text Token_Set_Ratio"]:
                    worksheets[worksheet_name].write(0, count, s, cell_format)
                    count = count + 1

                myfoo = 1
                for imgx in Statics.FILES_GRABBED:
                    real_result = get_required_text(imgx)
                    mydat = Statics.INPUT_FOLDER + imgx
                    result = m.MY_RESULTS[mydat]["result"]
                    dirty_result = m.MY_RESULTS[mydat]["dirty_result"]
                    (Ratio, Partial_Ratio, Token_Sort_Ratio, Token_Set_Ratio) = self.similar(real_result, result)
                    (Ratio2, Partial_Ratio2, Token_Sort_Ratio2, Token_Set_Ratio2) = self.similar(real_result,
                                                                                                 dirty_result)
                    table2.rows.append(
                        [str(imgx), real_result, result, Ratio, Partial_Ratio, Token_Sort_Ratio, Token_Set_Ratio,
                         dirty_result, Ratio2, Partial_Ratio2, Token_Sort_Ratio2, Token_Set_Ratio2])
                    count = 0
                    for s in [str(imgx), real_result, result, Ratio, Partial_Ratio, Token_Sort_Ratio, Token_Set_Ratio,
                         dirty_result, Ratio2, Partial_Ratio2, Token_Sort_Ratio2, Token_Set_Ratio2]:
                        # print(i)

                        worksheets[worksheet_name].write(myfoo, count, s)
                        count = count+1
                    myfoo = myfoo + 1
                Statics.LOGGER.logme(table2)
                self.filecreation(table, str(m.__class__.__name__)+"_RESULT_DETAILS_" + timex+".txt",timex)
                Statics.LOGGER.logme(
                    "--------------------------------------------------------------------------------------")

        workbook.close()



    def open_as_webpage(self):
        pass
