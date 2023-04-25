from tkinter import OFF
from matplotlib.text import OffsetFrom
from numpy import size


def Find_defects(imgin):
    import numpy as np
    import matplotlib.pyplot as plt
    from PIL import Image
    import tensorflow as tf
    from tensorflow import keras
    from keras.models import Model
    from keras.layers import Conv2D, MaxPooling2D, Input, Conv2DTranspose, Concatenate, BatchNormalization, UpSampling2D
    from keras.layers import  Dropout, Activation
    import cv2
   

    from tensorflow.python.platform.tf_logging import error
    def make_squarebw(img):
        #Getting the bigger side of the image
        s = max(img.shape[0:2])
        #Creating a white square   
        f = np.zeros((s,s),np.uint8)
        #Getting the centering position
        ax,ay = (s - img.shape[1])//2,(s - img.shape[0])//2
        #Pasting the 'image' in a centering position
        f[ay:img.shape[0]+ay,ax:ax+img.shape[1]] = img
        return f
    def make_square(img):
        #Getting the bigger side of the image
        s = max(img.shape[0:2])
        #Creating a dark square with NUMPY  
        f = np.zeros((s,s,3),np.uint8)
        #Getting the centering position
        ax,ay = (s - img.shape[1])//2,(s - img.shape[0])//2
        #Pasting the 'image' in a centering position
        f[ay:img.shape[0]+ay,ax:ax+img.shape[1]] = img
        return f
    
    pre = imgin
    pre= np.array(pre)
    pre = make_square(pre)
    pre = cv2.resize(pre, dsize=(128, 128), interpolation=cv2.INTER_CUBIC)
    tam = cv2.cvtColor(pre, cv2.COLOR_RGB2HSV)
    tam = cv2.fastNlMeansDenoisingColored(tam,None,10,6,7,21)

    pre = pre.astype('float32')
    tam = tam.astype('float32')
    pre /=255
    tam /=255

    #load model
    model = keras.models.load_model('model.h5')
    
    #predict the mask 
    pred = model.predict(np.expand_dims(pre, 0))

    #mask processing 
    sum=0.0
    count=0
    h_const=0.35
    s_const= 1.3
    v_const=6
    avg_const=1.22
    constants=6 
    err_pixel = 0
    plus = 2
    mask  = pred.squeeze()
    mask = cv2.copyMakeBorder(mask, constants, constants, constants, constants, cv2.BORDER_CONSTANT,value=[0,0,0])
    mask = cv2.resize(mask, dsize=(128, 128), interpolation=cv2.INTER_CUBIC)
    mask = np.stack((mask,)*3, axis=-1)
    mask[mask >= 0.5] = 1 
    mask[mask < 0.5] = 0 
    M,N,k = mask.shape
    for i in range(0,M):
        for j in range(0,N):
            if (mask[i,j,0]==1):
                sum+=tam[i,j,0]*h_const+tam[i,j,1]*s_const+tam[i,j,2]*v_const
                count+=1
    avg=sum/count/avg_const
    ermsk=np.zeros((128,128,3),np.uint8)
    nemsk = cv2.copyMakeBorder(mask, 2,2,2,2, cv2.BORDER_CONSTANT,value=[0,0,0])
    newtam = cv2.copyMakeBorder(tam, 2,2,2,2, cv2.BORDER_CONSTANT,value=[0,0,0])

    for i in range(plus,M+plus):
        for j in range(plus,N+plus):
            if ((nemsk[i,j,0]>0.8) & (newtam[i,j,0]*h_const+newtam[i,j,1]*s_const+newtam[i,j,2]*v_const<avg)):
                lim = (plus*2+1)*(plus*2+1)-1
                xq = 0
                for a in range(-plus,plus+1):
                    for b in range(-plus,plus+1):
                        if (a,b != (0,0)):
                            if ((nemsk[i+a,j+b,0]>0.8) & (newtam[i+a,j+b,0]*h_const+newtam[i+a,j+b,1]*s_const+newtam[i+a,j+b,2]*v_const<avg)):
                                xq = xq + 1                
                if (xq/lim > 0.5):
                    err_pixel = err_pixel + 1
                    ermsk[i-plus,j-plus,0]=1
                    ermsk[i-plus,j-plus,1]=1
                    ermsk[i-plus,j-plus,2]=1

    #Negative ermsk 
    L = 1.0
    a = cv2.cvtColor(ermsk, cv2.COLOR_BGR2GRAY)
    for x in range(0, M):
        for y in range(0, N):
                r = a[x, y]
                s = L - r
                a[x, y] = s
    ermsk = cv2.cvtColor(a, cv2.COLOR_GRAY2BGR)

    # show the mask and the segmented image
    percent = round(err_pixel/count*100, 2)
    titles = 'Area defects: ' +  str(percent)+'%'
    imgout = np.concatenate([pre, ermsk, mask*ermsk], axis = 1)
    plt.figure(figsize=(6, 2), dpi= 150) 
    plt.axis('off')
    plt.title(titles)
    plt.imshow(imgout)
    plt.savefig('imgout.jpg')


