### Filename    : checkPrintSuccess.py
### Author      : Ron Bulaon
### Description : Check if the files sent to printer was printed successfuly

import os
import subprocess
from io import StringIO
import csv
from printLog import *
from subprocess import check_output
import time

def checkPrintSuccess(filename):
    time.sleep(3)
    try:
        defaultPrinter = check_output('wmic printer get name,default|findstr TRUE', shell=True).decode() # Get the configured defautl printer
        defaultPrinter = defaultPrinter.split('     ')[1]

        f = StringIO(check_output('wmic printjob get /format:csv', shell=True).decode()) # get all the printjob and its status on CSV format
        printQueue = csv.reader(f, delimiter=',')
    except:
        logThis('Error in checkPrintSuccess')
        return False

    x=1
    printedList = []
    for row in printQueue:
        if x>1 and (row[1] == defaultPrinter):                                  # Filter printjob results for the default printer only. Disregard the other printers.
            if (row[7] == filename) and (row[13] == 'Printed'):
                if filename not in printedList:
                    printedList.append(filename)                                # if the file has been printed successfuly append the filename to the printed list
            elif (row[7] == filename) and (row[13] != 'Printed'):
                deleteJobID = StringIO(check_output('wmic printjob where jobid=%s delete' % (row[12]), shell=True).decode()) # if the printed file is on the list but not printed successfuly, delete the printjob so the app can resend it later.
                if 'Instance deletion successful' in deleteJobID:
                    print('%s : Instance deletion successful' % (filename))
                    return False
        x+=1

    if filename in printedList:
        return True
    else:
        return False

    return False
