# PyTesser #

PyTesser is an Optical Character Recognition module for Python.  It takes as input an image or image file and outputs a string.

PyTesser uses the [Tesseract OCR engine](http://code.google.com/p/tesseract-ocr/), converting images to an accepted format and calling the Tesseract executable as an external script.  A Windows executable is provided along with the Python scripts.  The scripts should work in other operating systems as well.

### Dependencies ###

[PIL](http://www.pythonware.com/products/pil/) is required to work with images in memory.  PyTesser has been tested with Python 2.4 in Windows XP.

### Usage Example ###

```
>>> from pytesser import *
>>> image = Image.open('fnord.tif')  # Open image object using PIL
>>> print image_to_string(image)     # Run tesseract.exe on image
fnord
>>> print image_file_to_string('fnord.tif')
fnord
```

(more examples in [README](README.md))