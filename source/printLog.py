### Filename    : printLog.py
### Author      : Ron Bulaon
### Description : Logger function for the events. One log file a day.

import time
import os
import shutil
import configparser
from pathlib import Path
from datetime import datetime, timedelta

config = configparser.ConfigParser()
config.read('holdslipprinter.ini')

LOGRETENTION = int(config['LOG']['RETENTION'])
LOGFOLDER = config['LOG']['FOLDER']
LOGFOLDETPATH = os.path.abspath(LOGFOLDER)
PRINTEDFOLDER = 'printed'


def logFilename(days):                                                       # log filename generator referencing from today
    date = datetime.today() - timedelta(days=days)                           # generate date according depending on how many days has passed. Zero (0) means today.
    filename = 'printlog-%02d%02d%d.log' % (date.day, date.month, date.year) # generate string filename
    return filename

def delLogs(daysToKeep):                                                     # delete logs older than the number of days specified
    filesToKeep = []
    x=0

    if os.path.exists(LOGFOLDER):
        while x <= daysToKeep:                                  # if the file is older than the number of days specified
            filesToKeep.append(r'%s' % (logFilename(x)))        # keep the expected filename of the files to be kept
            x+=1

        dirlist = os.listdir(os.path.abspath(LOGFOLDER))        # get all files inside log folder
        if len(dirlist) > 0:
            for file in dirlist:
                if not file in filesToKeep:                     # check if the file is in the expected filename to keep
                    os.remove(os.path.join(LOGFOLDETPATH,file)) # if not delete the log file
    filesToKeep = []

    return


def delFiles(daysToKeep):                                                                                                       # delete pritned files older than the days to keep setting
    if os.path.exists(LOGFOLDER) and (daysToKeep > 0):                                                                          # do this if the log file has contents and the days to keep a file is greater than zero
        for each in os.listdir(os.path.abspath(PRINTEDFOLDER)):                                                                 # get all files in the printed folder
            if (int(os.path.getctime(os.path.join(os.path.abspath(PRINTEDFOLDER),each)) - time.time())) > (daysToKeep * 86400): # check if the file age is less than the days to keep setting
                os.remove(os.path.getctime(os.path.join(os.path.abspath(PRINTEDFOLDER),each))) # if the
    return


def logThis(logMsg):
    Path(LOGFOLDER).mkdir(parents=True, exist_ok=True)

    try:
        delLogs(LOGRETENTION)
    except:
        print('unable to remove old logs')

    try:
        delFiles(LOGRETENTION)
    except:
        print('unable to delete old PDFs')

    try:
        dateTimeObj = datetime.now()
        log = open(r'%s' % (os.path.join(LOGFOLDETPATH,logFilename(0))),'a', encoding='utf-8')
        log.write('[%s] [%s]\n' % (dateTimeObj, logMsg))
        log.close()
    except:
        print(logMsg)

    return
