import cv2
import numpy as np
import colorsys
# DO NOT CHANGE THE NAME OF THIS METHOD OR ITS INPUT OUTPUT BEHAVIOR

# INPUT CONVENTION
# filenames: a list of strings containing filenames of images

# OUTPUT CONVENTION
# The method must return a list of strings. Make sure each string is either "ODD"
# or "EVEN" (without the quotes) depending on whether the hexadecimal number in
# the image is odd or even. Take care not to make spelling or case mistakes. Make
# sure that the length of the list returned as output is the same as the number of
# filenames that were given as input. The judge may give unexpected results if this
# convention is not followed.

    
def cropFN(image):
    j=image.shape[1]
    cnt=0
    while(cnt<4):
        j=j-1
        cnt=0
        for i in range(image.shape[0]):
            if(image[i][j]==0):
                cnt=cnt+1
    end=j
    down=0
    up=image.shape[0]
    while(cnt>=4):
        j=j-1
        cnt=0
        for i in range(image.shape[0]):
            if(image[i][j]==0):
                cnt=cnt+1
                up=min(up,i)
                down=max(down,i)
    start=j
    return image[up:down,start:end]

def BnW(image):
    thresh=cv2.inRange(image,(0,0,0),(127,127,127))
    output=cv2.bitwise_not(thresh)
    return output


def prediction(c):
    if(c=='0' or c=='2' or c=='4' or c=='6' or c=='8' or c=='A' or c=='C' or c=='E'):
        return('EVEN')
    return('ODD')


def compFN(image1,image2,mine):
    error=0
    for i in range(2,68):
        for j in range(2,68):
            if(image1[i][j]!=image2[i][j]):
                error=error+1
        if(error>=mine):
            return 4900
    return error

def decaptcha( filenames ):
    # Invoke your model here to make predictions on the images
    labels=[]
    l=['A','B','C','D','E','F','0','1','2','3','4','5','6','7','8','9']
    names=['n30','n20','n10','n0','p10','p20','p30']
    n=len(filenames)
    for i1 in range(n):
        in_image=cv2.imread(filenames[i1])
        in_image=cv2.cvtColor(in_image,cv2.COLOR_BGR2HSV)
        thresh=cv2.inRange(in_image,(0,0,0),(255,255,160))
        output=cv2.bitwise_not(thresh)
        final=cropFN(output)
        final=cv2.resize(final,(70,70))
        mine=1500
        pred='A'
        for i in l:
            for j in names:
                s=i+j+'.png'
                image=cv2.imread(s)
                image=BnW(image)
                image=cv2.resize(image,(70,70))
                error=compFN(image,final,mine)
                if(error<mine):
                    mine=error
                    pred=i
        c=prediction(pred)
        labels.append(c)
    return labels
