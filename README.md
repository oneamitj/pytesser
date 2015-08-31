Introduction:
============
PyTesser is an Optical Character Recognition module for Python. It takes 
as input an image or image file and outputs a string.

PyTesser uses the Tesseract OCR engine (an Open Source project at Google), 
converting images to an accepted format and calling the Tesseract 
executable as an external script. A Windows executable is provided 
along with the Python scripts. The scripts should work in Linux as well. 

+ PyTesser:

>https://github.com/wannamit/pytesser/

>http://code.google.com/p/pytesser/

+ Tesseract:

>http://code.google.com/p/tesseract-ocr/


Dependencies:
=============
- PIL is required to work with images in memory.
>https://pypi.python.org/pypi/Pillow/
- This version of PyTesser has been tested with Python 3.4 in Windows 10 and Python 2.7 in Ubuntu 14.04 LTS.
- For Linux:
	+ Add executable permission to all .exe file `chmod +x dlltest.exe tesseract.exe`
	+ Install wine `sudo apt-get install wine`
	+ Execute `winetricks  mfc42`


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
	... 	text = image_file_to_string("my_tif_image", graceful_errors=False)
	... except errors.Tesser_General_Exception, value:
	... 	print("`tif_image` is incompatible filetype.  Try graceful_errors=True")
	... 	print(value)
	... 	

`tif image file` is incompatible filetype.  Try graceful_errors=True
Tesseract Open Source OCR Engine
read_tif_image:Error:Illegal image format:Compression
Tessedit:Error:Read of file failed:fnord.tif
Signal_exit 31 ABORT. LocCode: 3  AbortCode: 3


File Dependencies:
============================================
- __pytesser.py__	Main module for importing
- __util.py__		Utility functions used by pytesser.py
- __errors.py__	Interprets exceptions thrown by Tesseract
- __tesseract.exe__	Executable called by pytesser.py
- __tessdata/__	Resources used by tesseract.exe

pdf2jpg.py
=============================================
This file is a pdf to jpg converter written by Ned Batchelder and original Py2 code can be found [here](http://nedbatchelder.com/blog/200712/extracting_jpgs_from_pdfs.html)

###Usage

	python3 pdf2jpg.py <path_of_pdf_file>
	

pdf2txt.py
=============================================
###Usage

	python pdf2txt.py pdf1 pdf2 pdf3 (...so on)

Output will be files named `<pdf_name>_pg#.txt` in the txt folder.
