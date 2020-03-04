# HoldSlipPrinter
[Alma](https://www.exlibrisgroup.com/products/alma-library-services-platform/) is a cloud solution for libraries. And because this service is hosted on the cloud, it does not have access to local printers attached on the devices where it is accessed. The common solution and [workaround](https://developers.exlibrisgroup.com/blog/using-thunderbird-as-a-print-proxy/) is to use [Thunderbird](https://www.thunderbird.net/) as a print proxy for printing Hold Slips. In this regard, **HoldSlipPrinter** aims to even simplify printing hold slips by removing the graphical interface and just run this script as a print daemon in the background.

### Advantages
1. There is no graphical interface i.e. Less distraction and less point of error.
2. Configuration/Settings are located in a single configuration file.
3. Print output is smaller than my Thunderbird work around.

### Here's a simplified things that this solution will do:
1. Check for new emails with hold request notification.
2. If there's a new email, download and save it for printing at request folder.
3. Then send the saved requests (in PDF) to the printer.
4. If printing is successful move the file from request folder to printed folder.
5. Repeat the entire process.


## How to use this:
You have two options to choose from:
1. Easy way : Download and configure the compiled versions on compiled directory.
2. Compile a copy : Clone this repository and compile your own version.

### Easy Way:
These instructions does not cover installation of your printer. This app will send files to the default printer set on the operating system level. This will work with any printer you set as default. I'm using EPSON TM-T82
1. Download the compiled version of [holdslipprinter.zip](https://github.com/smu-libraries/HoldSlipPrinter/blob/master/compiled/holdslipprinter.zip) and extract contents.
2. Edit in your settings at the configuration file holdslipprinter.ini.
    ```
    [DEFAULT]
    mylocation = Li Ka Shing Library
    email = your_email@domain.edu.sg
    username = DOMAIN\userid
    password = secure_password

    [MAIL]
    subject = Resource Request Slip
    from = sender@domain.edu.sg

    [MISC]
    count = 20

    [LOG]
    folder = logs
    retention = 2
    ```
    holdslipprinter.ini must be in the same directory as app.exe. Fill and change values as needed:
     * **mylocation** - In my case we have multiple location and we only wanted to print for the location where the printer is located. This entry must be searchable within the body of the email.
     * **email** - email address for the mailbox where you receive the hold slip requests
     * **username** - login account for the mailbox. The same account you used for checking this mailbox.
     * **password** - password for the mailbox. This should be the same password you use to access the email.
     * **subject** - subject of the email of the hold requests
     * **from** - email address of the sender of the hold request i.e. the email alma used for sending the hold request.
     * **count** - number of emails to be check. Example if you put 20, the 1st 20 emails will be checked.
     * **folder** - folder name of the log file destination
     * **retention** - number of days to keep the log files.
3. Open Windows' [Task Scheduler](https://docs.microsoft.com/en-us/windows/win32/taskschd/using-the-task-scheduler), create and configure a basic task to run app.exe at each computer startup. Here's the settings I've used for your reference. This part may differ depending on PC setup/environment.
     * **General Tab** <br> ![general](/img/image1.png)
     * **Triggers Tab** <br> ![general](/img/image2.png)
     * **Actions Tab** <br> ![general](/img/image3.png)
4. On the printer settings, set the printer to keep printed documents. This will prevent the printer to print multiple copies of the slips. Here's how I set mine:
     * **Advance Tab of printer settings** <br> ![printer settings](/img/image7.png)
5. This step is optional but recommended to run these scripts at least once a day.
     * **deletePrintedPDF.bat** will delete the printed PDFs at printed folder. If you want to archive all the printed files, then you do not have to run this script. You can go to the printed folder too to re-print any previously printed slips.
     * **restartSpooler.bat** This script will clear all the printed logs at the printer's print queue. If you have low volume of printouts you can schedule this to once a week. Mine is on daily.

     Here's how I set mine:
      * **General Tab** <br> ![general](/img/image4.png)
      * **General Tab** <br> ![general](/img/image5.png)
      * **General Tab** <br> ![general](/img/image6.png)

      _Note : I did these settings for both scripts and the scripts assumes that the folders' location is at Program Files._

### Compile a copy:
Before compiling your own version follow the Easy Way instructions above. Then do the following:
1. Clone this repository.
    ```
    git clone https://github.com/smu-libraries/HoldSlipPrinter.git
    ```
2. Go to the downloaded repository's source folder and install the requirements.
    ```
    cd source
    ```

    ```
    pip install -r Requirements.txt
    ```
3. Compile to an executable.
    ```
    pyinstaller --noconsole --nowindowed -F app.py
    ```
4. PyInstaller will create a dist folder and you should be able to find app.exe inside. Copy app.exe and replace the file app.exe file you have from [holdslipprinter.zip](https://github.com/smu-libraries/HoldSlipPrinter/blob/master/compiled/holdslipprinter.zip).

### Acknowldements :
I have used [WK<html>TOPDF](https://wkhtmltopdf.org/downloads.html) to convert HTML files to PDF. Check their [github page here](https://github.com/wkhtmltopdf/wkhtmltopdf). For sending files to printer I've used [PDFtoPRinter](http://www.columbia.edu/~em36/pdftoprinter.html). This program will send PDFs to printer from a windows command line.

### Other Ideas:
* What about a version of this on a headless single board PCs?

### Copyright
Copyright (c) 2020 Ron Ron Bulaon <br>
Licensed under the MIT License(MIT). See LICENSE.md for more info.
