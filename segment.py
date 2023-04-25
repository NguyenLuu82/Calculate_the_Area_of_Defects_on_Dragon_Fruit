import cv2
import glob
from PIL import Image
import numpy as np
import os 
from pathlib import Path
import imp
import copy
L=256
def make_squarebw(img):
    #Getting the bigger side of the image
    s = max(img.shape[0:2])

    #Creating a white square with NUMPY  
    f = np.zeros((s,s),np.uint8)

    #Getting the centering position
    ax,ay = (s - img.shape[1])//2,(s - img.shape[0])//2

    #Pasting the 'image' in a centering position
    f[ay:img.shape[0]+ay,ax:ax+img.shape[1]] = img
    return f
def make_square(img):
    #Getting the bigger side of the image
    s = max(img.shape[0:2])

    #Creating a white square with NUMPY  
    f = np.zeros((s,s,3),np.uint8)

    #Getting the centering position
    ax,ay = (s - img.shape[1])//2,(s - img.shape[0])//2

    #Pasting the 'image' in a centering position
    f[ay:img.shape[0]+ay,ax:ax+img.shape[1]] = img
    return f
def segment(imgin):
    imgin = cv2.fastNlMeansDenoisingColored(imgin,None,15,10,7,21)
    imgin = cv2.cvtColor(imgin, cv2.COLOR_BGR2GRAY)
    imgout = imgin
    M, N = imgin.shape
    heso = 1.35
    av = heso*(np.average(imgin))
    for x in range(0,M):
        for y in range(0,N):
            if (imgout[x,y]>av):
                imgout[x,y]=0
            else:
                imgout[x,y]=255
    return imgout
working_dir = Path()
filename=[]
for path in working_dir.glob("train_128//**/*.jpg"):
    filename.append(path)
count=1000
for file in filename:
    img = str(file)
    n= cv2.imread(img)
    bw=copy.copy(n)
    bw = segment(bw)
    n = make_square(n)
    n = cv2.resize(n, (128,128), interpolation = cv2.INTER_AREA)
    bw = make_squarebw(bw)
    bw = cv2.resize(bw, (128,128), interpolation = cv2.INTER_AREA)
    cv2.imwrite('predt\\'+str(count)+str(0)+'.jpg',n)

    cv2.imwrite('dttrain\\'+str(count)+str(1)+'.jpg',bw)
    cv2.imwrite('mask\\'+str(count)+str(1)+'.jpg',bw)
    print('dttrain\\'+str(count)+str(1)+'.jpg')
    count+=1