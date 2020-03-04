### Filename    : app.py
### Author      : Ron Bulaon
### Description : check for unread emails, save it to HML, convert to PDF, then send to printer

from htmlToPDF import htmlToPDF, filesToPDF
from getMail import writeHTML, checkMail
from pdfToPrinterprinter import printPDF, moveToPrinted, filesToPrinter
from pathlib import Path
import configparser
import os
import time
from printLog import *

def checkConfigFile():                      # Chcek for config file. Create a default holdslipprinter.ini if not found
    CONFIGFILE = 'holdslipprinter.ini'
    config = configparser.ConfigParser()
    if not os.path.exists(CONFIGFILE):
        config['DEFAULT'] = {
            'mylocation' : '<LOCATION>',    # Physical location of the printer
            'email' : '<EMAIL>',            # Email to get the hold slips from
            'username' : '<USERNAME>',      # user name for email
            'password' : '<PASSWORD>'       # password for email
            }

        config['MAIL'] = {
            'subject'   :   '<EMAIL SUBJECT>',  # subject of the email. To be used for filtering email
            'from'      :   '<EMAIL SENDER>'    # hold slip sender email address
            }

        config['MISC'] = {
            'count'     :   3                   # number of emails to be checked i.e. first 3 emails
            }

        config['LOG'] = {
            'folder' : 'logs',
            'retention' : '3'
        }


        with open (CONFIGFILE, 'w') as CONFIGFILE:
            config.write(CONFIGFILE)

        logThis('%s has just beeen created. Please update it before starting application' % (CONFIGFILE))

    else:
        config.read('holdslipprinter.ini')
        if (config['DEFAULT']['MYLOCATION'] == '<LOCATION>') or (config['DEFAULT']['EMAIL'] == '<EMAIL>') or (config['DEFAULT']['USERNAME'] == '<USERNAME>') or (config['DEFAULT']['PASSWORD'] == '<PASSWORD>') or (config['MAIL']['SUBJECT'] == '<EMAIL SUBJECT>') or (config['MAIL']['FROM'] == '<EMAIL SENDER>') :
            logThis('You need to update %s before starting application' % (CONFIGFILE))
            return False

        return {    'mylocation'  : config['DEFAULT']['MYLOCATION'],
                    'email'       : config['DEFAULT']['EMAIL'],
                    'username'    : config['DEFAULT']['USERNAME'],
                    'password'    : config['DEFAULT']['PASSWORD'],
                    'subject'     : config['MAIL']['SUBJECT'],
                    'from'        : config['MAIL']['FROM'],
                    'count'       : config['MISC']['COUNT'],
        }

    return False

def app():
    try:
        Path('printed').mkdir(parents=True, exist_ok=True)  # create pinted folder if missing
        Path('requests').mkdir(parents=True, exist_ok=True) # create requests folder if missing
        Path('logs').mkdir(parents=True, exist_ok=True)     # create logs folder if missing
    except:
        print('Please check write permissions!')
        exit()

    files = ['PDFtoPrinterSelect.exe','wkhtmltoimage.exe','wkhtmltopdf.exe','wkhtmltox.dll','PDFtoPrinter.exe']
    folder = 'bin'

    if not os.path.exists(folder):
        print('Fatal Error : bin folder not found!')
        exit()
    else:
        folder = os.path.abspath(folder)
        for file in files:
            if not os.path.exists(os.path.join(folder,file)):
                print('Fatal Error : %s not found!' % (file))
                exit()

    configs = checkConfigFile()
    if not configs:
        print('Error loading credentials')
        exit()

    while True:
        checkMail(configs['mylocation'],configs['email'],configs['username'],configs['password'],configs['subject'],configs['from'],configs['count'])
        filesToPDF()        # check if there's any HTML file to convert to PDF
        filesToPrinter()    # check for any PDF files. If found send it to printer
        time.sleep(5)       # wait for 5 seconds before retrying

    return

app()
