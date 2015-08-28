from PIL import Image
import subprocess
import os
import io
import sys

import util
import errors


tesseract_exe_name = 'dlltest.exe' # Name of executable to be called at command line
scratch_image_name = "temp.bmp" # This file must be .bmp or other Tesseract-compatible format
scratch_text_name_root = "temp" # Leave out the .txt extension
_cleanup_scratch_flag = True  # Temporary files cleaned up after OCR operation
_language = "" # Tesseract uses English if language is not given
_pagesegmode = "" # Tesseract uses fully automatic page segmentation if psm is not given (psm is available in v3.01)

_working_dir = os.getcwd()

def call_tesseract(input_filename, output_filename, language, pagesegmode):
	"""Calls external tesseract.exe on input file (restrictions on types),
	outputting output_filename+'txt'"""
	current_dir = os.getcwd()
	error_stream = io.StringIO()
	try:
		os.chdir(_working_dir)

		if sys.platform == 'win32': #For windows based OS
			args = [tesseract_exe_name, input_filename, output_filename]
		else: #For unix based OS
			args = ['wine',tesseract_exe_name, input_filename, output_filename]

		if len(language) > 0:
			args.append("-l")
			args.append(language)
		if len(str(pagesegmode)) > 0:
			args.append("-psm")
			args.append(str(pagesegmode))
		try:
			proc = subprocess.Popen(args)
		except (TypeError, AttributeError):
			proc = subprocess.Popen(args, shell=True)
		retcode = proc.wait()
		

		if retcode!=0:
			error_text = error_stream.getvalue()
			errors.check_for_errors(error_stream_text = error_text)
	finally:  # Guarantee that we return to the original directory
		error_stream.close()
		os.chdir(current_dir)

def image_to_string(im, lang = _language, psm = _pagesegmode, cleanup = _cleanup_scratch_flag):
	"""Converts im to file, applies tesseract, and fetches resulting text.
	If cleanup=True, delete scratch files after operation."""
	try:
		util.image_to_scratch(im, scratch_image_name)
		call_tesseract(scratch_image_name, scratch_text_name_root, lang, psm)
		result = util.retrieve_result(scratch_text_name_root)
	finally:
		if cleanup:
			util.perform_cleanup(scratch_image_name, scratch_text_name_root)
	return result

def image_file_to_string(filename, lang = _language, psm = _pagesegmode, cleanup = _cleanup_scratch_flag, graceful_errors=True):
	"""Applies tesseract to filename; or, if image is incompatible and graceful_errors=True,
	converts to compatible format and then applies tesseract.  Fetches resulting text.
	If cleanup=True, delete scratch files after operation. Parameter lang specifies used language.
	If lang is empty, English is used. Page segmentation mode parameter psm is available in Tesseract 3.01.
	psm values are:
	0 = Orientation and script detection (OSD) only.
	1 = Automatic page segmentation with OSD.
	2 = Automatic page segmentation, but no OSD, or OCR
	3 = Fully automatic page segmentation, but no OSD. (Default)
	4 = Assume a single column of text of variable sizes.
	5 = Assume a single uniform block of vertically aligned text.
	6 = Assume a single uniform block of text.
	7 = Treat the image as a single text line.
	8 = Treat the image as a single word.
	9 = Treat the image as a single word in a circle.
	10 = Treat the image as a single character."""
	try:
		try:
			call_tesseract(filename, scratch_text_name_root, lang, psm)
			result = util.retrieve_result(scratch_text_name_root)
		except errors.Tesser_General_Exception:
			if graceful_errors:
				im = Image.open(filename)
				result = image_to_string(im, cleanup)
			else:
				raise
	finally:
		if cleanup:
			util.perform_cleanup(scratch_image_name, scratch_text_name_root)
	return result
	

# if __name__=='__main__':
# 	im = Image.open('phototest.tif')
# 	text = image_to_string(im, cleanup=False)
# 	print(text)
# 	text = image_to_string(im, psm=2, cleanup=False)
# 	print(text)
# 	try:
# 		text = image_file_to_string('fnord.tif', graceful_errors=False)
# 	except errors.Tesser_General_Exception as value:
# 		print("fnord.tif is incompatible filetype.  Try graceful_errors=True")
# 		#print value
# 	text = image_file_to_string('fnord.tif', graceful_errors=True, cleanup=False)
# 	print("fnord.tif contents:", text)
# 	text = image_file_to_string('fonts_test.png', graceful_errors=True)
# 	print(text)
# 	text = image_file_to_string('fonts_test.png', lang="eng", psm=4, graceful_errors=True)
# 	print(text)



