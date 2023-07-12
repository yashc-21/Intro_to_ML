import cv2
import numpy
import colorsys
import matplotlib.pyplot as plt
import easyocr
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


def show_image(image):
    rgb_image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    plt.axis("off")
    plt.imshow(rgb_image)

    
def cropFN(image):
    j=image.shape[1]
    cnt=0
    while(cnt<4):
        j=j-1
        cnt=0
        for i in range(image.shape[0]):
            if(image[i][j]==0):
                cnt=cnt+1
    while(cnt>=4):
        j=j-1
        cnt=0
        for i in range(image.shape[0]):
            if(image[i][j]==0):
                cnt=cnt+1
    while(cnt<4):
        j=j-1
        cnt=0
        for i in range(image.shape[0]):
            if(image[i][j]==0):
                cnt=cnt+1
    return image[:,j:]


def prediction(c):
    if(c=='0' or c=='2' or c=='4' or c=='6' or c=='8' or c=='A' or c=='C' or c=='E'):
        return('EVEN')
    return('ODD')


def BnW(image):
    thresh=cv2.inRange(image,(0,0,0),(255,90,255))
    output=cv2.bitwise_not(thresh)
    return output


def remLines(image):
    k=cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
    erosion=cv2.erode(inv_image,k,iterations=4)
    output=cv2.bitwise_not(erosion)
    return output


def decaptcha( filenames ):
    # Invoke your model here to make predictions on the images
    labels=[]
    n=len(filenames)
    for i in range(n):
        in_image=cv2.imread(filenames[i])
        in_image=cv2.cvtColor(in_image,cv2.COLOR_BGR2HSV)
        in_image=BnW(in_image)
        output=remLines(in_image)
        final=cropFN(output)
        final = cv2.equalizeHist(output)
        final = cv2.GaussianBlur(output, (5, 5), 1)
        reader= easyocr.Reader(['en'])
        result = reader.readtext(final,paragraph="False", allowlist='0123456789ABCDEF')
        labels.append(prediction(result[0][1]))
    return labels
