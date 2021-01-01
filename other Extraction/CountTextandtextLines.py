# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 20:19:34 2020

@author: BPAVA
"""


import PyPDF2
import string

# pdf file object
# you can find find the pdf file with complete code in below
pdfFileObj = open('1.pdf', 'rb')
# pdf reader object
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
# number of pages in pdf
print(pdfReader.numPages)
# a page object
pageObj = pdfReader.getPage(0)
# extracting text from page.
# this will print the text you can also save that into String
#print(pageObj.extractText())

count = 0
counter = 0

for line in pageObj.extractText().translate({ord(c): None for c in string.whitespace}).strip():  # splitlines() for lines and Strip() for each
    # characters
    count += 1

for textline in pageObj.extractText().replace(" ", "").splitlines():
    counter += 1
print("No. of Text Characters",count)
print("No. of Text Lines",counter)