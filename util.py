"""Utility functions for processing images for delivery to Tesseract"""

import os
import re

_add_dot_txt_flag = False


def image_to_scratch(im, scratch_image_name):
	"""Saves image in memory to scratch file.  .bmp format will be read correctly by Tesseract"""
##	if im.mode=='RGBA':
##		im=im.convert('RGB')
##	try:
##		im.save(scratch_image_name, dpi=(200,200))
##	except:  ### Eventually this should catch only the specific im.save exception
##		im = im.convert('RGB')
##		im.save(scratch_image_name, dpi=(200,200))
	#im = im.convert('1')
	im.save(scratch_image_name, dpi=(200,200))

def	retrieve_text(scratch_text_name_root):
	if _add_dot_txt_flag:
		inf = open(scratch_text_name_root + '.txt')
	else:
		inf = open(scratch_text_name_root)
	text = inf.read().strip()
	inf.close()
	return text

# Eventually this more thorough class should be used:

##class OCR_character:
##	"""Object exposing internals of Tesseract result for particular characters
##	(See documentation of EANYCODE_CHAR
##	http://tesseract-ocr.googlecode.com/svn&cs_f=trunk/ccutil/ocrclass.h
##	for detailed explanations)
##	self.letter - OCRed letter guess
##	self.char_code - Character code of letter
##	self.x_bounds - (left bound, right bound)
##	self.y_bounds - (top bound, bottom bound)
##	self.font_index - Index of character's font
##	self.confidence - 0 (low conf) to 100 (high)
##	self.point_size - Estimated size of font (units unclear)
##	self.formatting - Bit flags for formatting and layout information
##	"""
##	def __init__(self, line):
##		data = line.split(' ')
##		self.letter = data[0]
##		self.char_code = int(data[1], 16)
##		self.x_bounds = (data[2], data[4])
##		self.y_bounds = (data[5], data[3])
##		self.font_index = data[6]
##		self.confidence = data[7]
##		self.point_size = data[8]
##		self.formatting = data[9]
##	def __str__(self):
##		return self.letter

# This simple class is used for now:

class OCR_character:
	"""Object exposing internals of Tesseract result for particular characters
	(See documentation of EANYCODE_CHAR
	http://tesseract-ocr.googlecode.com/svn&cs_f=trunk/ccutil/ocrclass.h
	for detailed explanations)
	self.letter - OCRed letter guess
	self.x_bounds - (left bound, right bound)
	self.y_bounds - (top bound, bottom bound)
	"""
	def __init__(self, line):
		parse_re = re.compile(r'^(.).*\((.+),(.+)\).*\((.+),(.+)\)') # Match example 'T[54]->[54](35,115)->(56,90)'
		data = parse_re.findall(line)[0]
		self.letter = data[0]
		self.x_bounds = (int(data[1]), int(data[3]))
		self.y_bounds = (int(data[2]), int(data[4]))
	

class OCR_result(str):
	"""Parsed results of call to Tesseract; subclass of 'str'.
	self OCR string.
	self.internals is array (aligned with self.text) of OCR_letter
		internal data objects (for characters) or None (for whitespace,
		since Tesseract provides no internal data for whitespace characters)."""
	def __new__(self, text):
		raw_letters = []
		internals = []
		data = text.split('\n')
		i = 0
		while i<len(data):
			line = data[i].strip()
			if line=='<nl>':  # New line
				raw_letters.append('\n')
				internals.append(None)
				i += 1
			elif line=='<para>':  # End of input
				break
			elif line=='':  # Space character
				raw_letters.append(' ')
				internals.append(None)
			else:
				character = OCR_character(line)
				raw_letters.append(character.letter)
				internals.append(character)
			i += 1
		self = str.__new__(self, "".join(raw_letters))
		self.internals = internals
		return self
			
	
def retrieve_result(scratch_text_name_root):
	text = retrieve_text(scratch_text_name_root)
	return OCR_result(text)

def perform_cleanup(scratch_image_name, scratch_text_name_root):
	"""Clean up temporary files from disk"""
	if _add_dot_txt_flag:
		scratch_text_name = scratch_text_name_root + '.txt'
	else:
		scratch_text_name = scratch_text_name_root
	for name in (scratch_image_name, scratch_text_name, "tesseract.log"):
		try:
			os.remove(name)
		except OSError:
			pass
