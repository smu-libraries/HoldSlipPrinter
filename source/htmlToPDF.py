### Filename    : htmlToPDF.py
### Author      : Ron Bulaon
### Description : Convert *.html files found in request/ folder to PDF format

from pathlib import Path
import pdfkit
import os
from printLog import *


def htmlToPDF(folder,file):                                                     # convert the html file on the folder specified to pdf format

    path_wkhtmltopdf = str(os.path.abspath('bin'))+'\\wkhtmltopdf.exe'          # check if the HTML to PDF converter is available
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    options = {
        'dpi'           : '400',                                                # DPI setting 400 - 600
        'page-size'     : 'B7',                                                 # paper size and other settings
        'margin-top'    : '5',
        'margin-right'  : '20',
        'margin-left'   : '1',
    }

    if os.path.exists(folder):                                                  # check if the folder exist
        filename_html = os.path.join(os.path.abspath(folder),file)              # get the absolute path of the file
        filename_pdf = filename_html.replace('.html','.pdf')                    # generate filename for the output i.e. PDF file
        if not os.path.exists(filename_html):
            print ('Error : %s\\%s is missing' % (folder,file))
            return False
    else:
        logThis('Error : bin %s is missing' % (folder))
        return False

    try:
        logThis('converting %s to PDF' % (filename_html))
        pdfkit.from_file(filename_html, filename_pdf,configuration=config,options=options)  # actual conversion command
    except:
        logThis('Could not convert %s to %s ' % (filename_html, filename_pdf))
        return False
    else:
        if os.path.exists(filename_pdf):                                        # check if the pdf file is successfuly generated
            logThis('Deleting %s' % (filename_html))
            os.remove(filename_html)                                            # if PDF file is successfuly generated, delete the html file
            return True
        else:
            logThis('Error : Could not create %s' % (filename_pdf))
            return False

    return False

def filesToPDF(defaultFolder='requests'):                                       # check if there's hml file ont he request folder.
    logThis('checking %s\\ folder for pending HTML to convert' % (defaultFolder))
    if os.path.exists(defaultFolder):
        for file in os.listdir(defaultFolder):                                  # get all contents of the folder
            if len(os.listdir(defaultFolder)) <=0:                              # nothing to do if there's no file in folder
                logThis('No PDF files found')
                return False

            logThis('converting %s to PDF' % (file))
            htmlToPDF(defaultFolder,file)                                       # if the folder is not empty, conver the files to PDF
            return True                                                         # return successful
    else:
        print ('Error : %s is missing' % (defaultFolder))
        return False

    return False
