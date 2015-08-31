# !/usr/bin/env python
'''
@Author Amit Joshi
'''

from pytesser import *
from pdf2jpg import *

for pdf in sys.argv[1:]:
	print('Processing PDFs...\n')
	pdf2jpg(pdf)

jpgs = os.listdir('tmp')
print('\nProcessing JPEGs...')
print('Completed Count')
count = 0

for jpg in jpgs:
	img = Image.open('tmp/'+jpg)
	txt = image_to_string(img)

	if not os.path.isdir('txt'):
		os.system('mkdir txt')
	f = open('txt/'+jpg.replace('.jpg','.txt'), 'w')
	f.write(txt)
	f.close()
	count += 1
	print(str(count)+'\t'),
	os.system('rm tmp/'+jpg)

print("\n\nDONE, see txt folder for results.")
