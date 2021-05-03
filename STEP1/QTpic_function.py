from math import *
from cv2 import cv2
import numpy as np
import os
import torchvision.transforms as transforms
from PIL import Image

def contrast_img(img1,c,b):
    rows,cols,channels=img1.shape
    blank=np.zeros([rows,cols,channels],img1.dtype)
    dst=cv2.addWeighted(img1,c,blank,1-c,b)
    return dst

def rot(image,image_width,image_height,angle):
    image_heightNew = int(image_width * fabs(sin(radians(angle))) + image_height * fabs(cos(radians(angle))))
    image_widthNew = int(image_height * fabs(sin(radians(angle))) + image_width * fabs(cos(radians(angle))))

    center = (image_width/2,image_height/2)
    M = cv2.getRotationMatrix2D(center, angle, 1)

    M[0,2] += (image_widthNew - image_width)/2
    M[1,2] += (image_heightNew - image_height)/2

    rotated = cv2.warpAffine(image,M,(image_widthNew, image_heightNew), borderValue = (255, 255, 255))
    return rotated

def rotate(pic_path, save_path, low, high):
    file=os.listdir(pic_path)
    for i in file:
        if (".jpg" in n)or(".png" in n)or(".JPG" in n)or(".jpeg" in n):
            image = cv2.imread(pic_path+i)
            image_height, image_width = image.shape[0:2]
            if(low<high):
                for angle in range(low,high+1):
                    rotated = rot(image,image_width,image_height,angle)
                    cv2.imwrite(save_path+i[:-4]+"_angle"+str(angle)+".jpg", rotated)
            else:
                for angle in range(low,361):
                    rotated = rot(image,image_width,image_height,angle)
                    cv2.imwrite(save_path+i[:-4]+"_angle"+str(angle)+".jpg", rotated)
                for angle in range(0,high+1):
                    rotated = rot(image,image_width,image_height,angle)
                    cv2.imwrite(save_path+i[:-4]+"_angle"+str(angle)+".jpg", rotated)    



def bright(pic_path, save_path, minBright, maxBright, mincontrast, maxcontrast):
    file=os.listdir(pic_path)
    for bright in range(minBright,maxBright+1,1):
        for contrast in np.arange(mincontrast,maxcontrast+0.05,0.1):
            contrast = round(contrast,1)
            
            for i in file:    
                if (".jpg" in n)or(".png" in n)or(".JPG" in n)or(".jpeg" in n):
                    image = cv2.imread(pic_path+i)
                    _contrast = contrast_img(image,contrast,bright) 
                    cv2.imwrite(save_path+i[:-4]+"_"+str(bright)+"_"+str(contrast)+"_"+".jpg",_contrast)  
                else:
                    continue

def resize(pic_path, save_path, min_width, max_width, min_height, max_height):
    file=os.listdir(pic_path)
    for i in file:
        if (".jpg" in n)or(".png" in n)or(".JPG" in n)or(".jpeg" in n):
            for width in range(min_width, max_width+1):
                for height in range(min_height, max_height+1):
                    image = cv2.imread(pic_path+i)
                    imagescale = cv2.resize(image, (width, height))
                    cv2.imwrite(save_path+i[:-4]+".jpg",imagescale)
        else:
            continue

def shift(pic_path, save_path, min_shift_right, max_shift_right, min_shift_down, max_shift_down):
    file=os.listdir(pic_path)
    for i in file:
        if (".jpg" in n)or(".png" in n)or(".JPG" in n)or(".jpeg" in n):
            for shift_right in range(min_shift_right, max_shift_right+1):
                for shift_down in range(min_shift_down, max_shift_down+1):
                    image = cv2.imread(pic_path+i)
                    image_height, image_width = image.shape[0:2]
                    M = np.float32([[1,0,shift_right], [0,1,shift_down]]) 
                    dst = cv2.warpAffine(image, M, (image_width, image_height), borderValue=(255,255,255))
                    cv2.imwrite(save_path+i[:-4]+"_"+str(shift_right)+"_"+str(shift_down)+"_"+str('shift')+".jpg",dst)
                else:
                    continue

def flip(pic_path,save_path,min_flipValue, max_flipValue):
    file=os.listdir(pic_path)
    for i in file:
        if (".jpg" in n)or(".png" in n)or(".JPG" in n)or(".jpeg" in n):
            image = cv2.imread(pic_path+i)
            xImg = cv2.flip(image,flipValue,dst=None)
            cv2.imwrite(save_path+i[:-4]+"_"+str(flipValue)+"_"+str('flip')+".jpg",xImg)
        else:
            continue

def hue(pic_path, save_path, pic_counts, hue_low, hue_high):
    file=os.listdir(pic_path)
    for pic_count in range(pic_counts):
        for n in file:
            extension = n.split('.')
            pic_name = extension[0]
            for i in range (1,len(extension)-1):
                pic_name = pic_name + "." + extension[i]
            if (".jpg" in n)or(".png" in n)or(".JPG" in n)or(".jpeg" in n):
                img = Image.open(pic_path + n).convert('RGB')
                trainTransform = transforms.Compose([
                transforms.ColorJitter(hue=[hue_low, hue_high])])
                
                img = trainTransform(img)
                image = np.array(img)
                save_image_path = save_path + pic_name + "_" + str(pic_count) + "_hue" + '.' + str(extension[len(extension)-1])
                
                img.save(save_image_path)
                img.close()