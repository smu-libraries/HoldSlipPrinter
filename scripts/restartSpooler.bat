@ECHO OFF
net stop spooler
del %systemroot%\system32\spool\printers\* /Q /F
net start spooler
