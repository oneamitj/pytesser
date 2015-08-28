Introduction:
============
PyTesser is an Optical Character Recognition module for Python. It takes 
as input an image or image file and outputs a string.

PyTesser uses the Tesseract OCR engine (an Open Source project at Google), 
converting images to an accepted format and calling the Tesseract 
executable as an external script. A Windows executable is provided 
along with the Python scripts. The scripts should work in Linux as well. 

PyTesser:
https://github.com/wannamit/pytesser/
http://code.google.com/p/pytesser/
Tesseract:
http://code.google.com/p/tesseract-ocr/


Dependencies:
=============
PIL is required to work with images in memory. This version of PyTesser has been tested with Python 3.4 in Windows 10. 
https://pypi.python.org/pypi/Pillow/


Installation:
==============
No installation. Just download - import - use.

Usage:
================================
>>> from pytesser import *
>>> img = Image.open("my_image_path")
>>> text = image_to_string(img)
>>> print text

>>> try:
... 	text = image_file_to_string('fnord.tif', graceful_errors=False)
... except errors.Tesser_General_Exception, value:
... 	print "fnord.tif is incompatible filetype.  Try graceful_errors=True"
... 	print value
... 	
fnord.tif is incompatible filetype.  Try graceful_errors=True
Tesseract Open Source OCR Engine
read_tif_image:Error:Illegal image format:Compression
Tessedit:Error:Read of file failed:fnord.tif
Signal_exit 31 ABORT. LocCode: 3  AbortCode: 3

>>> text = image_file_to_string('fnord.tif', graceful_errors=True)
>>> print "fnord.tif contents:", text
fnord.tif contents: fnord

>>> text = image_file_to_string('fonts_test.png', graceful_errors=True)
>>> print text
12 pt
And Arnazwngw few dwscotheques provwde jukeboxes
Tames Amazmgly few dnscotheques pmvxde Jukeboxes
24 pt:
Arial: Amazingly few discotheques
provide jul<ebo><es.
Courier: Ama zimgly few
discotheque S provide
j u k e b ox e S .
Times: Amazingly few discotheques provide
jukeboxes.


File Dependencies:
============================================
pytesser.py	Main module for importing
util.py		Utility functions used by pytesser.py
errors.py	Interprets exceptions thrown by Tesseract
tesseract.exe	Executable called by pytesser.py
tessdata/	Resources used by tesseract.exe
