### Filename    : getMail.py
### Author      : Ron Bulaon
### Description : Check for any unread email. Save it as HTML if relevant emails are found.

from exchangelib import DELEGATE, Account, Credentials
from pathlib import Path
from checkPrintSuccess import checkPrintSuccess
from datetime import datetime
import re
import os
from printLog import *

def writeHTML(requestID,emailBody,defaultFolder='requests'):                    # save the body of the email in HTML file. Note: body of the email is already on HTML
    logThis('Saving %s from email in html format' % (requestID))
    Path(defaultFolder).mkdir(parents=True, exist_ok=True)                      # create request folder or defaultfolder if the folder does not exist
    filename = r'requests//'+str(requestID)+'.html'
    if os.path.exists(filename) is not True:
        try:
            f = open(r'%s' % (filename), 'w', encoding='utf-8')                 # Open file for writing
            f.write(emailBody)                                                  # write body of the email to the file
            f.close()                                                           # save and close the file
            logThis('%s created' % (filename))
        except IOError:
            logThis("File not accessible")
            return False
        finally:
            f.close()
            return False

    return True

def checkMail(MYLOCATION,EMAIL,USERNAME,PASSWORD,SUBJECT,FROM,COUNT):
    logThis('checking email...')

    # use the credentials below to access email
    try:
        creds = Credentials(
            username=USERNAME,
            password=PASSWORD)

        account = Account(
            primary_smtp_address=EMAIL,
            credentials=creds,
            autodiscover=True,
            access_type=DELEGATE)
    except:
        logThis('Error reading email : please check credentials')

    try:
        for item in account.inbox.all().filter(subject=SUBJECT, sender=FROM, is_read=False)[:int(COUNT)]: # check the first nth (COUNT) unread emails with the subject and sender as filter.
            emailBody = item.body
            if MYLOCATION in emailBody:                                         # if body of the email contains the current location get the request ID.
                try:
                     requestID = re.search('Request ID: (.+?)</span>', emailBody).group(1) # look for the request ID in the body of the email
                except AttributeError:
                    requestID = ''
                    return False

                if not checkPrintSuccess(str(requestID)+'.pdf'):                # check if request ID has been printed already.
                    if writeHTML(requestID,emailBody):                          # if not yet printed save the emailBody as HTML
                        item.is_read = True                                     # and mark the email as read
                        item.save()                                             # then save the mailbos change.
                        time.sleep(0.5)                                         # wait for a while to allow mailbox changing to take effect
                        logThis('%s' % (emailBody))
                        requestID = ''                                          # clear request ID and emailbody
                        emailBody = ''
                        return True
                else:
                    item.is_read = True                                         # if email has printed already. mark it as read.
                    item.save()                                                 # save the email setting
                    logThis('marked %s as read' % (str(requestID)))

        requestID = ''                                                          # clear request ID and emailbody
        emailBody = ''
    except:
        logThis('Error in checking email : please check credentials or network connection')

    return False
