"""Utility functions for processing images for delivery to Tesseract"""

import os

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
	im = im.convert('1')
	im.save(scratch_image_name, dpi=(200,200))

def	retrieve_text(scratch_text_name_root):
	if _add_dot_txt_flag:
		inf = file(scratch_text_name_root + '.txt')
	else:
		inf = file(scratch_text_name_root)
	text = inf.read().strip()
	inf.close()
	return text

class OCR_character:
	"""Object exposing internals of Tesseract result for particular characters
	(See documentation of EANYCODE_CHAR
	http://tesseract-ocr.googlecode.com/svn&cs_f=trunk/ccutil/ocrclass.h
	for detailed explanations)
	self.letter - OCRed letter guess
	self.char_code - Character code of letter
	self.x_bounds - (left bound, right bound)
	self.y_bounds - (top bound, bottom bound)
	self.font_index - Index of character's font
	self.confidence - 0 (low conf) to 100 (high)
	self.point_size - Estimated size of font (units unclear)
	self.formatting - Bit flags for formatting and layout information
	"""
	def __init__(self, line):
		data = line.split(' ')
		self.letter = data[0]
		self.char_code = int(data[1], 16)
		self.x_bounds = (data[2], data[4])
		self.y_bounds = (data[5], data[3])
		self.font_index = data[6]
		self.confidence = data[7]
		self.point_size = data[8]
		self.formatting = data[9]
	def __str__(self):
		return self.letter
		

class OCR_result:
	"""Parsed results of call to Tesseract.
	self.text is OCR string.
	self.internals is array (aligned with self.text) of OCR_letter
		internal data objects (for characters) or None (for whitespace,
		since Tesseract provides no internal data for whitespace characters)."""
	def __init__(self, text):
		raw_letters = []
		self.internals = []
		data = text.split('\n')
		i = 0
		while i<len(data):
			line = data[i].strip()
			if line=='<nl>':  # New line
				raw_letters.append('\n')
				self.internals.append(None)
				i += 1
			elif line=='<para>':  # End of input
				break
			elif line=='':  # Space character
				raw_letters.append(' ')
				self.internals.append(None)
			else:
				character = OCR_character(line)
				raw_letters.append(character.letter)
				self.internals.append(character)
			i += 1
		self.text = ''.join(raw_letters)
	def __str__(self):
		return self.text
			
	
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
