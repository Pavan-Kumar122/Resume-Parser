import zipfile
import shutil
from os import listdir
from os.path import isfile, join
import numpy
import cv2
import docx2txt

docxpath = 'Prerana_Rath.docx'
docx2txt.process(docxpath, "C:\\Users\\BPAVA\\OneDrive\\Desktop\\resume_parser\\resume-parser-master\\image")  # for extracting the images


imagepath = "C:\\Users\\BPAVA\\OneDrive\\Desktop\\resume_parser\\resume-parser-master\\image"
onlyfiles = [f for f in listdir(imagepath) if isfile(join(imagepath, f))]
images = numpy.empty(len(onlyfiles), dtype=object)
for n in range(0, len(onlyfiles)):
    images[n] = cv2.imread(join(imagepath, onlyfiles[n]))  # for storing the image in the list


# checking the images whether there is image or not
count = 1
for imagedata in onlyfiles:
    image = cv2.imread("C:\\Users\\BPAVA\\OneDrive\\Desktop\\resume_parser\\resume-parser-master\\image\\"+imagedata)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=3,
        minSize=(30, 30)
    )
    value = format(len(faces))
    if value > '0':
        status = cv2.imwrite('image' + str(count) + '.jpg', image)
        print(f'[INFO] Image image{count}.jpg written to filesystem: ', status)
        count += 1

