import cv2
import numpy
import colorsys
import matplotlib.pyplot as plt

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


def rotateFN(image,deg):
    image=cv2.bitwise_not(image)
    height,width=image.shape[:2]
    rotation_matrix=cv2.getRotationMatrix2D((width/2,height/2),deg,1)
    rotated_image1=cv2.warpAffine(image,rotation_matrix,(width,height))
    rotated_image=cv2.bitwise_not(rotated_image1)
    return rotated_image


l=['A','B','C','D','E','F','0','1','2','3','4','5','6','7','8','9']
deg=[-30,-20,-10,0,10,20,30]
names=['n30','n20','n10','n0','p10','p20','p30']
for i in l:
    s='reference/'+i+'.png'
    image=cv2.imread(s)
    #image=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    image=BnW(image)
    for j in range(7):
        rotated_image=rotateFN(image,deg[j])
        final=cropFN(rotated_image)
        s1='112/'+i+names[j]+'.png'
        cv2.imwrite(s1,final)
