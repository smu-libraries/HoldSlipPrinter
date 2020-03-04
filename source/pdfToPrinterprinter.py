### Filename    : pdfToPrinterprinter.py
### Author      : Ron Bulaon
### Description : check if tehre's any PDF file to the request/ folder
###               and send it to the default printer. Move file to rpinted folder.

import os
import subprocess
import win32ui
import win32print
import win32con
import shutil
from pathlib import Path
from checkPrintSuccess import checkPrintSuccess
from printLog import *


def printPDF(filenamePDF,defaultFolder='requests',defaultPrinter='default'):    # Check bin foler and PDFtoPrinter exists and on the expected location

    if os.path.exists('bin'):
        PDFtoPrinter = os.path.join(os.path.abspath('bin'),'PDFtoPrinter.exe')  # get he full path of the PDF file printer
        if not os.path.exists(PDFtoPrinter):
            logThis ('Error : bin\\PDFtoPrinter.exe is missing')
            return False
    else:
        logThis ('Error : bin folder is missing')
        return False

    if os.path.exists(defaultFolder):                                           # Check if the defaultFolder exisit and the PDF file exists
        printFile = os.path.join(os.path.abspath(defaultFolder),filenamePDF)    # full path of the file to be printed
        if not os.path.exists(printFile):
            logThis('Error : %s\\%s is missing' % (defaultFolder,filenamePDF))
            return False
    else:
        logThis('Error : %s folder is missing' % defaultFolder)
        return False

    # Check printer
    if defaultPrinter == 'default':
        defaultPrinter = win32print.GetDefaultPrinter()                         # getthe default printer
        if defaultPrinter is None:
            logThis('Error : No default printer or no printer installed')
            return False
    else:
        if not defaultPrinter in win32print.EnumPrinters(5):                    # check if the default printer is in the list of installed printers
            logThis ('Error : %s is not installed' % (defaultPrinter))
            return False

    try:
        logThis('sending %s to printer' % (filenamePDF))
        p = subprocess.Popen([PDFtoPrinter, printFile], stdout=subprocess.PIPE, stderr=subprocess.PIPE) # actual command for sending the PDF fiel to the printer
        stdout, stderr = p.communicate()
        return True
    except:
        return False

    return False

def moveToPrinted(filenamePDF,defaultFolder='requests',printedFolder='printed'):    # move the printed file from request/ to printed/

    Path(printedFolder).mkdir(parents=True, exist_ok=True)                          # if printed/ folder does not exist, create it.

    if os.path.exists(printedFolder):
        printFile = os.path.join(os.path.abspath(defaultFolder),filenamePDF)        # full path of the pdf file
        if not os.path.exists(printFile):
            logThis('Error : %s\\%s is missing' % (defaultFolder,filenamePDF))
            return False
        else:
            shutil.move(printFile,printFile.replace(defaultFolder,printedFolder))   # command to mvoe the printed pdf file from request/ to printed
            logThis('Moving %s to %s' % (printFile,printedFolder))
    else:
        logThis ('Error : %s folder is missing' % defaultFolder)
        return False


def filesToPrinter(defaultFolder='requests'):                                       # send all contents of request/ folder to the printer
    if os.path.exists(defaultFolder):                                               # check if the folder exist
        for file in os.listdir(defaultFolder):                                      # get allfiles inside the
            if '.pdf' in file:                                                      # check each file if its on PDF file type
                logThis('Found %s to in request\\ folder.' % (file))
                if printPDF(file):                                                  # print the pdf file
                        if checkPrintSuccess(file):                                 # check if the files has been printed successfuly
                            moveToPrinted(file)                                     # if the *.pdf has been printed successfuly, move the fiel to printed folder
                            return True
                        else:
                            logThis('Error : printer printing error')
                            return False
    else:
        logThis('Error : %s is missing' % (defaultFolder))
        return False

    return False
