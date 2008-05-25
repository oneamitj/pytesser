"""OCR in Python using the Tesseract engine from Google
http://code.google.com/p/pytesser/
by Michael J.T. O'Kelly
V 0.0.1, 3/10/07"""

import Image
import subprocess
import os
import StringIO

import util
import errors


tesseract_exe_name = 'dlltest-mod' # Name of executable to be called at command line
scratch_image_name = "temp.bmp" # This file must be .bmp or other Tesseract-compatible format
scratch_text_name_root = "temp" # Leave out the .txt extension
_cleanup_scratch_flag = True  # Temporary files cleaned up after OCR operation

_working_dir = os.getcwd()

def call_tesseract(input_filename, output_filename):
	"""Calls external tesseract.exe on input file (restrictions on types),
	outputting output_filename+'txt'"""
	current_dir = os.getcwd()
	error_stream = StringIO.StringIO()
	try:
		os.chdir(_working_dir)
		args = [tesseract_exe_name, input_filename, output_filename]
		try:
			proc = subprocess.Popen(args,stderr=error_stream, shell=True)
		except TypeError:
			proc = subprocess.Popen(args, shell=True)
		retcode = proc.wait()
		if retcode!=0:
			error_text = error_stream.getvalue()
			errors.check_for_errors(error_stream_text = error_text)
	finally:  # Guarantee that we return to the original directory
		error_stream.close()
		os.chdir(current_dir)

def image_to_string(im, cleanup = _cleanup_scratch_flag):
	"""Converts im to file, applies tesseract, and fetches resulting text.
	If cleanup=True, delete scratch files after operation."""
	try:
		util.image_to_scratch(im, scratch_image_name)
		call_tesseract(scratch_image_name, scratch_text_name_root)
		result = util.retrieve_result(scratch_text_name_root)
	finally:
		if cleanup:
			util.perform_cleanup(scratch_image_name, scratch_text_name_root)
	return result

def image_file_to_string(filename, cleanup = _cleanup_scratch_flag, graceful_errors=True):
	"""Applies tesseract to filename; or, if image is incompatible and graceful_errors=True,
	converts to compatible format and then applies tesseract.  Fetches resulting text.
	If cleanup=True, delete scratch files after operation."""
	try:
		try:
			call_tesseract(filename, scratch_text_name_root)
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
	

if __name__=='__main__':
	im = Image.open('phototest.tif')
	text = image_to_string(im, cleanup=False)
	print text
	try:
		text = image_file_to_string('fnord.tif', graceful_errors=False)
	except errors.Tesser_General_Exception, value:
		print "fnord.tif is incompatible filetype.  Try graceful_errors=True"
		print value
	text = image_file_to_string('fnord.tif', graceful_errors=True, cleanup=False)
	print "fnord.tif contents:", text
	text = image_file_to_string('fonts_test.png', graceful_errors=True)
	print text


