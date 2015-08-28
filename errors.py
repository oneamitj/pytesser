"""Test for exceptions raised in the tesseract.exe logfile"""

class Tesser_General_Exception(Exception):
	pass

class Tesser_Invalid_Filetype(Tesser_General_Exception):
	pass

def check_for_errors(logfile = "tesseract.log", error_stream_text = ""):
	try:
		inf = open(logfile)
		error_stream_text += inf.read()
		inf.close()
	except IOError:
		pass
	# All error conditions result in "Error" somewhere in logfile
	if error_stream_text.lower().find("error") != -1:
		raise Tesser_General_Exception(error_stream_text)