#資料夾內只能為同一物件 filename = objectName-objectType.filetype
from math import fabs, sin, cos, radians
from cv2 import cv2
import numpy as np
import os
import csv  
import torchvision.transforms as transforms
from PIL import Image

#亮度 function
def contrast_img(img1,c,b):
    rows,cols,channels=img1.shape
    #新建全零圖片陣列src2,將height和width，型別設定為原圖片的通道型別(色素全為零，輸出為全黑圖片)
    blank=np.zeros([rows,cols,channels],img1.dtype)
    dst=cv2.addWeighted(img1,c,blank,1-c,b)#合成圖片
    return dst

def rotateFilename(filename, angle):
    temp = filename.split('.')
    if len(temp) > 2:    
        newFilename = str(temp[0])
        for extraPoint in range(1,len(temp)-1):
            newFilename = newFilename + "." + str(temp[extraPoint])
        newFilename = newFilename + "_" + str(angle) + "_rotate" + "." + str(temp[len(temp)-1])
    else:
        newFilename = str(temp[0]) + "_" + str(angle) + "_rotate" + "." + str(temp[1])
    return newFilename

def brightFilename(filename, bright, contrast):
    temp = filename.split('.')
    if len(temp) > 2:    
        newFilename = str(temp[0])
        for extraPoint in range(1,len(temp)-1):
            newFilename = newFilename + "." + str(temp[extraPoint])
        newFilename = newFilename + "_" + str(bright) + "_" + str(contrast) + "_bright" + "." + str(temp[len(temp)-1])
    else:
        newFilename = str(temp[0]) + "_" + str(bright) + "_" + str(contrast) + "_bright" + "." + str(temp[1])
    return newFilename

def resizeFilename(filename, width, height):
    temp = filename.split('.')
    if len(temp) > 2:    
        newFilename = str(temp[0])
        for extraPoint in range(1,len(temp)-1):
            newFilename = newFilename + "." + str(temp[extraPoint])
        newFilename = newFilename + "_" + str(width) + "_" + str(height) + "_scale" + "." + str(temp[len(temp)-1])
    else:
        newFilename = str(temp[0]) + "_" + str(width) + "_" + str(height) + "_scale" +"." + str(temp[1])
    return newFilename

# 0: filename 1:file_size 2: file_attributes 3: region_count 4: region_id 5: region_shape_attribute 6: region   
def shiftFilename(filename, shift_right, shift_down):
    temp = filename.split('.')
    if len(temp) > 2:    
        newFilename = str(temp[0])
        for extraPoint in range(1,len(temp)-1):
            newFilename = newFilename + "." + str(temp[extraPoint])
        newFilename = newFilename + "_" + str(shift_right) + "_" + str(shift_down) + "_shift" + "." + str(temp[len(temp)-1])
    else:
        newFilename = str(temp[0]) + "_" + str(shift_right) + "_" + str(shift_down) + "_shift" + "." + str(temp[1])
    return newFilename

def flipFilename(filename, flipValue):
    temp = filename.split('.')
    if len(temp) > 2:    
        newFilename = str(temp[0])
        for extraPoint in range(1,len(temp)-1):
            newFilename = newFilename + "." + str(temp[extraPoint])
        newFilename = newFilename + "_" + str(flipValue) + "_flip" + "." + str(temp[len(temp)-1])
    else:
        newFilename = str(temp[0]) + "_" + str(flipValue) + "_flip" + "." + str(temp[1])
    return newFilename

def hueFilename(filename, pic_count):
    temp = filename.split('.')
    if len(temp) > 2:    
        newFilename = str(temp[0])
        for extraPoint in range(1,len(temp)-1):
            newFilename = newFilename + "." + str(temp[extraPoint])
        newFilename = newFilename + "_" + str(pic_count) + "_hue" + "." + str(temp[len(temp)-1])
    else:
        newFilename = str(temp[0]) + "_" + str(pic_count) + "_hue" + "." + str(temp[1])
    return newFilename

def rot(image,image_width,image_height,angle):
    image_heightNew = int(image_width * fabs(sin(radians(angle))) + image_height * fabs(cos(radians(angle))))
    image_widthNew = int(image_height * fabs(sin(radians(angle))) + image_width * fabs(cos(radians(angle))))

    center = (image_width//2,image_height//2)
    M = cv2.getRotationMatrix2D(center, angle, 1) 

    M[0,2] += (image_widthNew - image_width)//2
    M[1,2] += (image_heightNew - image_height)//2
    
    # M: 轉換矩陣, widthNew: 轉換後圖像尺寸, borderValue: 轉換後空白區域填充色 
    rotated = cv2.warpAffine(image,M,(image_widthNew, image_heightNew), borderValue = (255, 255, 255))
    return rotated,M

def rotate(pic_path, save_path, low, high):
    file=os.listdir(pic_path)
    count = 0
    if low > high:
        low = low - 360
    for angle in range(low, high+1, 20):
        with open(pic_path+"test_labels.csv", newline='') as csvfile:   # newline=''參數，讓資料中包含的換行字元可以正確被解析以迴圈輸出每一列
            rows = list(csv.reader(csvfile))
            tempCsvFilename = []
            tempCsvFilename = rows[1][0].split('-')
            csvFilename = save_path + str(tempCsvFilename[0]) + "_rotate.csv" 
            for n in file:
                extension = n.split('.')
                pic_name = extension[0]
                for i in range (1,len(extension)-1):
                    pic_name = pic_name + "." + extension[i]
                if (".jpg" in n)or(".png" in n)or(".JPG" in n)or(".jpeg" in n):
                    image = cv2.imread(pic_path+n)
                    image_height, image_width = image.shape[0:2]   
                    rotated, matRotation = rot(image,image_width,image_height,angle)
                    cv2.imwrite(save_path+pic_name+"_"+str(angle)+"_rotate"+"."+str(extension[len(extension)-1]), rotated)
                
                    y = 1
                    first = 1
                    duplicateFirst = 0
                    exist = False
                    for i in range(1,len(rows)):         # 尋找照片對應csv檔檔名
                        if n == str(rows[i][0]):        # 檢查檔銘是否相同
                            first = i
                            exist = True
                            if (i+1!=len(rows))and(rows[i][0] == rows[i+1][0])or(rows[i][0] == rows[i-1][0]):  # 檢查下一列   一樣為多物件
                                if(rows[i][0]!=rows[i-1][0]):
                                    y = i - 1
                                    duplicateFirst = i      
                                y = y + 1 
                            else:
                                y = first 
                    if (exist==True):    # check csv have pic label or not 
                        if(duplicateFirst>0):
                            first = duplicateFirst
                        # 0: filename 1:width 2: height 3: class 4: xmin 5: ymin 6: xmax 7:ymax
                        for x in range(first, y+1):
                            xmin = int(rows[x][4])
                            ymin = int(rows[x][5])
                            xmax = int(rows[x][6])
                            ymax = int(rows[x][7])
                            point1 = np.dot(matRotation,np.array([[xmin],[ymin],[1]]))
                            point2 = np.dot(matRotation,np.array([[xmax],[ymin],[1]]))
                            point3 = np.dot(matRotation,np.array([[xmax],[ymax],[1]]))
                            point4 = np.dot(matRotation,np.array([[xmin],[ymax],[1]]))
                            
                            new_image_height, new_image_width = rotated.shape[0:2]
                            
                            rows[x][1] = int(new_image_width)
                            rows[x][2] = int(new_image_height)
                            rows[x][4] = int(min(point1[0][0], point2[0][0], point3[0][0], point4[0][0]))
                            rows[x][5] = int(min(point1[1][0], point2[1][0], point3[1][0], point4[1][0]))
                            rows[x][6] = int(max(point1[0][0], point2[0][0], point3[0][0], point4[0][0]))
                            rows[x][7] = int(max(point1[1][0], point2[1][0], point3[1][0], point4[1][0]))
                            rows[x][0] = rotateFilename(rows[x][0], angle)
                            
                            #cv2.rectangle(rotated, (rows[x][4],rows[x][5]), (rows[x][6],rows[x][7]), (0,0,255), 1)
                        #cv2.imwrite(save_path + pic_name + "_after_" + str(angle)+ "_rotate." + str(extension[len(extension)-1]),rotated)
                    
            addcount = 0 
            with open(csvFilename, "a", newline='') as wcsvfile: # csv標頭
                writer = csv.writer(wcsvfile)
                for row in rows:
                    if (count!=0)and(addcount==0):            # 不是第一次寫入
                        addcount = addcount + 1
                        continue
                    writer.writerow(row)
                    addcount = addcount + 1
                count = count + 1
    



def bright(pic_path,save_path,minBright,maxBright,mincontrast,maxcontrast):     
    file=os.listdir(pic_path)
    count = 0       # 判斷是否要寫標頭
    for bright in range(minBright,maxBright+1,5):
        for contrast in np.arange(mincontrast,maxcontrast+0.05,0.1):
            contrast = round(contrast,1)
            with open(pic_path+"test_labels.csv", newline='') as csvfile:   # newline=''參數，讓資料中包含的換行字元可以正確被解析以迴圈輸出每一列
                rows = list(csv.reader(csvfile))
                # tempCsvFilename = []
                # tempCsvFilename = rows[1][0].split('-')
                csvFilename = save_path + "test_labels_bright.csv"
                for n in file:
                    extension = n.split('.')
                    pic_name = extension[0]
                    for i in range (1,len(extension)-1):
                        pic_name = pic_name + "." + extension[i]
                    if (".jpg" in n)or(".png" in n)or(".JPG" in n)or(".jpeg" in n):
                        image = cv2.imread(pic_path+n)
                        _contrast = contrast_img(image,contrast,bright) # (原始像素,對比度,亮度值)
                        
                        cv2.imwrite(save_path+pic_name+"_"+str(bright)+"_"+str(contrast)+"_"+str('bright')+"."+str(extension[len(extension)-1]),_contrast)
                            
                        y = 1
                        first = 1
                        duplicateFirst = 0
                        exist = False       # check csv have pic label or not 
                        for i in range(1,len(rows)):         # 尋找照片對應csv檔檔名
                            if n == str(rows[i][0]):        #檢查檔銘是否相同
                                first = i
                                exist = True
                                if (i+1!=len(rows))and(rows[i][0] == rows[i+1][0])or(rows[i][0] == rows[i-1][0]):  #檢查下一列   一樣為多物件
                                    if(rows[i][0]!=rows[i-1][0]):
                                        y = i - 1
                                        duplicateFirst = i      
                                    y = y + 1 
                                else:
                                    y = first 
                        if (exist==True):
                            if (duplicateFirst>0):
                                first = duplicateFirst
                            # 0: filename 1:file_size 2: file_attributes 3: region_count 4: region_id 5: region_shape_attribute 6: region
                            
                            for x in range(first, y+1):
                                rows[x][0] = brightFilename(rows[x][0], bright, contrast)
                                #cv2.rectangle(_contrast, (int(rows[x][4]),int(rows[x][5])), (int(rows[x][6]),int(rows[x][7])), (0,0,255), 1)
                            #cv2.imwrite(save_path + pic_name + "_after_" + str(bright) + "_" + str(contrast) + "_bright." + str(extension[len(extension)-1]),_contrast)
                addcount = 0 
                with open(csvFilename, "a", newline='') as wcsvfile: # csv標頭
                    writer = csv.writer(wcsvfile)
                    for row in rows:
                        if (count!=0)and(addcount==0):            # 不是第一次寫入
                            addcount = addcount + 1
                            continue
                        writer.writerow(row)
                        addcount = addcount + 1
                    count = count + 1
            


def resize(pic_path, save_path, minwidth, maxwidth, minheight, maxheight):
    file=os.listdir(pic_path)
    count = 0       # 判斷是否要寫標頭
    for width in range(minwidth, maxwidth+1):
        for height in range(minheight, maxheight+1):
            with open(pic_path+"test_labels.csv", newline='') as csvfile:   # newline=''參數，讓資料中包含的換行字元可以正確被解析以迴圈輸出每一列
                rows = list(csv.reader(csvfile))
                tempCsvFilename = []
                tempCsvFilename = rows[1][0].split('-')
                csvFilename = save_path + str(tempCsvFilename[0]) + "_resize.csv" 
                for n in file:
                    extension = n.split('.')
                    pic_name = extension[0]
                    for i in range (1,len(extension)-1):
                        pic_name = pic_name + "." + extension[i]
                    if (".jpg" in n)or(".png" in n)or(".JPG" in n)or(".jpeg" in n):
                        image = cv2.imread(pic_path+n)
                        image_height, image_width = image.shape[0:2]
                        imagescale = cv2.resize(image, (width, height)) 
                        cv2.imwrite(save_path+pic_name+"_"+str(width)+"_"+str(height)+"_"+str('scale')+"."+str(extension[len(extension)-1]),imagescale)
                        
                        y = 1
                        first = 1
                        duplicateFirst = 0
                        for i in range(1,len(rows)):         # 尋找照片對應csv檔檔名
                            if n == str(rows[i][0]):        #檢查檔銘是否相同
                                first = i
                                if (i+1!=len(rows))and(rows[i][0] == rows[i+1][0])or(rows[i][0] == rows[i-1][0]):  #檢查下一列   一樣為多物件
                                    if(rows[i][0]!=rows[i-1][0]):
                                        y = i - 1
                                        duplicateFirst = i      
                                    y = y + 1 
                                else:
                                    y = first 
                        
                        if(duplicateFirst>0):
                            first = duplicateFirst
                        # 0: filename 1:file_size 2: file_attributes 3: region_count 4: region_id 5: region_shape_attribute 6: region
                        for x in range(first, y+1):
                            xmin = int(int(rows[x][4])/(image_width/width))
                            ymin = int(int(rows[x][5])/(image_height/height))
                            xmax = int(int(rows[x][6])/(image_width/width))
                            ymax = int(int(rows[x][7])/(image_height/height))
                            
                            rows[x][0] = resizeFilename(rows[x][0], width, height)
                            cv2.rectangle(imagescale, (xmin,ymin), (xmax,ymax), (0,0,255), 2)
                        cv2.imwrite(save_path + pic_name + "_after_" + str(width) + "_" + str(height) + "_scale." + str(extension[len(extension)-1]),imagescale)
                addcount = 0 
                with open(csvFilename, "a", newline='') as wcsvfile: # csv標頭
                    writer = csv.writer(wcsvfile)
                    for row in rows:
                        if (count!=0)and(addcount==0):            # 不是第一次寫入
                            addcount = addcount + 1
                            continue
                        if addcount != (len(rows)):
                            writer.writerow(row)
                            addcount = addcount + 1
                    count = count + 1


def shift(pic_path, save_path, min_shift_right, max_shift_right, min_shift_down, max_shift_down):
    file=os.listdir(pic_path)
    count = 0       # 判斷是否要寫標頭
    for shift_right in range(min_shift_right, max_shift_right+1, 1):
        for shift_down in range(min_shift_down, max_shift_down+1, 1):
            outOfRangeCount = 0
            with open(pic_path+"test_labels.csv", newline='') as csvfile:   # newline=''參數，讓資料中包含的換行字元可以正確被解析以迴圈輸出每一列
                rows = list(csv.reader(csvfile))
                #tempCsvFilename = []
                #tempCsvFilename = rows[1][0].split('-')
                csvFilename = save_path + "test_labels_shift.csv"
                for n in file:
                    #平移圖片並儲存
                    extension = n.split('.')
                    pic_name = extension[0]
                    for i in range (1,len(extension)-1):
                        pic_name = pic_name + "." + extension[i]
                    if (".jpg" in n)or(".png" in n)or(".JPG" in n)or(".jpeg" in n):
                        image = cv2.imread(pic_path+n)
                        image_height, image_width = image.shape[0:2]
                        M = np.float32([[1,0,shift_right], [0,1,shift_down]]) 
                        dst = cv2.warpAffine(image, M, (image_width, image_height), borderValue=(255,255,255))
                        cv2.imwrite(save_path+pic_name+"_"+str(shift_right)+"_"+str(shift_down)+"_"+str('shift')+"."+str(extension[len(extension)-1]),dst)
                        #find data range
                        end = 0
                        first = 0
                        duplicateFirst = 0 #make duplicateFirst exist
                        for i in range(1,len(rows)-outOfRangeCount):         # 尋找照片對應csv檔檔名
                            if n == str(rows[i][0]):        #檢查檔名是否相同
                                first = i
                                if (i+1!=len(rows))and((rows[i][0] == rows[i+1][0])or(rows[i][0] == rows[i-1][0])):  #檢查下一列   一樣為多物件
                                    if (rows[i][0]!=rows[i-1][0]):      # 一張照片第一個
                                        end = i - 1       # y從i-1開始
                                        duplicateFirst = i
                                    end = end + 1
                                else:
                                    end = first
                        
                        if(duplicateFirst>0):
                            first = duplicateFirst

                        if(first==end==0):
                            continue

                        outOfRange = False
                        thisOutOfRangeCount = 0
                        for x in range(first, end+1):
                            xmin = int(rows[x-thisOutOfRangeCount][4]) + shift_right
                            ymin = int(rows[x-thisOutOfRangeCount][5]) + shift_down
                            xmax = int(rows[x-thisOutOfRangeCount][6]) + shift_right
                            ymax = int(rows[x-thisOutOfRangeCount][7]) + shift_down

                            rows[x-thisOutOfRangeCount][4] = xmin
                            rows[x-thisOutOfRangeCount][5] = ymin
                            rows[x-thisOutOfRangeCount][6] = xmax
                            rows[x-thisOutOfRangeCount][7] = ymax

                            outOfRange=False
                            if ((xmin < 0) or (ymin < 0)):        #檢查是否超出範圍
                                outOfRange = True
                            elif ((xmax > image_width)or(ymax > image_height)):
                                outOfRange = True

                            if outOfRange == True:# 超出範圍                
                                for i in range(x-thisOutOfRangeCount, len(rows)-1):           # 將outofrange row後面rows往前移
                                    for index in range(len(rows[i])):
                                        rows[i][index] = rows[i+1][index] 
                                outOfRangeCount = outOfRangeCount + 1
                                thisOutOfRangeCount = thisOutOfRangeCount + 1
                                continue
                            # 0: filename 1:file_size 2: file_attributes 3: region_count 4: region_id 5: region_shape_attribute 6: region
                            elif outOfRange == False:
                                rows[x-thisOutOfRangeCount][0] = shiftFilename(rows[x-thisOutOfRangeCount][0], shift_right, shift_down)
                                #cv2.rectangle(dst, (xmin,ymin), (xmax,ymax), (0,0,255), 2)
                                # circle(img, center, radius, color, thickness=None, lineType=None, shift=None)
                        cv2.imwrite(save_path + pic_name + "_after_" + str(shift_right) + "_" + str(shift_down) + "_shift." + str(extension[len(extension)-1]),dst)
                addcount = 0 
                with open(csvFilename, "a", newline='') as wcsvfile: # csv標頭
                    writer = csv.writer(wcsvfile)
                    for row in rows:
                        if (count!=0)and(addcount==0):            # 不是第一次寫入
                            addcount = addcount + 1
                            continue
                        if addcount != (len(rows)-outOfRangeCount):
                            writer.writerow(row)
                            addcount = addcount + 1
                        else:
                            break
                    count = count + 1


def flip(pic_path,save_path,minflipValue,maxflipValue):     # all_point_x,y有一些是str
    file=os.listdir(pic_path)
    count = 0       # 判斷是否要寫標頭
    for flipValue in range(minflipValue,maxflipValue+1):
        with open(pic_path+"test_labels.csv", newline='') as csvfile:   # newline=''參數，讓資料中包含的換行字元可以正確被解析以迴圈輸出每一列
            rows = list(csv.reader(csvfile))
            tempCsvFilename = []
            tempCsvFilename = rows[1][0].split('-')
            csvFilename = save_path + str(tempCsvFilename[0]) + "_flip.csv" 
            for n in file:
                extension = n.split('.')
                pic_name = extension[0]
                for i in range (1,len(extension)-1):
                    pic_name = pic_name + "." + extension[i]
                if (".jpg" in n)or(".png" in n)or(".JPG" in n)or(".jpeg" in n):
                    image = cv2.imread(pic_path+n)
                    image_height, image_width = image.shape[0:2]
                    xImg = cv2.flip(image,flipValue,dst=None)# 1水平鏡射 0垂直鏡射 -1：水平、垂直同時
                    cv2.imwrite(save_path+pic_name+"_"+str(flipValue)+"_"+str('flip')+"."+str(extension[len(extension)-1]),xImg)
                        
                    y = 1
                    first = 1
                    duplicateFirst = 0
                    for i in range(1,len(rows)):         # 尋找照片對應csv檔檔名
                        if n == str(rows[i][0]):        #檢查檔銘是否相同
                            first = i
                            if (i+1!=len(rows))and(rows[i][0] == rows[i+1][0])or(rows[i][0] == rows[i-1][0]):  #檢查下一列   一樣為多物件
                                if(rows[i][0]!=rows[i-1][0]):
                                    y = i - 1
                                    duplicateFirst = i      
                                y = y + 1 
                            else:
                                y = first 
                        
                    if(duplicateFirst>0):
                        first = duplicateFirst
                    # 0: filename 1:file_size 2: file_attributes 3: region_count 4: region_id 5: region_shape_attribute 6: region
                    
                    for x in range(first, y+1):
                        xmin = int(rows[x][4])
                        ymin = int(rows[x][5])
                        xmax = int(rows[x][6])
                        ymax = int(rows[x][7])

                        if flipValue == -1:
                            xmin = image_width - xmin
                            xmax = image_width - xmax          
                            ymin = image_height - ymin
                            ymax = image_height - ymax  
                        elif flipValue == 0:                
                            ymin = image_height - ymin
                            ymax = image_height - ymax
                        elif flipValue == 1:
                            xmin = image_width - xmin
                            xmax = image_width - xmax

                        rows[x][0] = flipFilename(rows[x][0], flipValue)
                        cv2.rectangle(xImg, (xmin,ymin), (xmax,ymax), (0,0,255), 2)
                    cv2.imwrite(save_path + pic_name + "_after_" + str(flipValue) + "_flip." + str(extension[len(extension)-1]),xImg)
                                                
            addcount = 0 
            with open(csvFilename, "a", newline='') as wcsvfile: # csv標頭
                writer = csv.writer(wcsvfile)
                for row in rows:
                    if (count!=0)and(addcount==0):            # 不是第一次寫入
                        addcount = addcount + 1
                        continue
                    if addcount != (len(rows)):
                        writer.writerow(row)
                        addcount = addcount + 1
                count = count + 1


def hue(pic_path, save_path, pic_counts, hue_low, hue_high):
    file=os.listdir(pic_path)
    count = 0       # 判斷是否要寫標頭
    for pic_count in range(pic_counts):
        with open(pic_path+"test_labels.csv", newline='') as csvfile:   # newline=''參數，讓資料中包含的換行字元可以正確被解析以迴圈輸出每一列
            rows = list(csv.reader(csvfile))
            tempCsvFilename = []
            tempCsvFilename = rows[1][0].split('-')
            csvFilename = save_path + str(tempCsvFilename[0]) + "_hue.csv" 
            for n in file:
                extension = n.split('.')
                pic_name = extension[0]
                for i in range (1,len(extension)-1):
                    pic_name = pic_name + "." + extension[i]
                if (".jpg" in n)or(".png" in n)or(".JPG" in n)or(".jpeg" in n):
                    img = Image.open(pic_path + n).convert('RGB')
                    trainTransform = transforms.Compose([
                    transforms.ColorJitter(hue=[hue_low, hue_high])]) # hue 色調
                    
                    img = trainTransform(img)
                    image = np.array(img)
                    #img.show()
                    save_image_path = save_path + pic_name + "_" + str(pic_count) + "_hue" + '.' + str(extension[len(extension)-1])
                    
                    img.save(save_image_path)
                    img.close()

                    y = 1
                    first = 1
                    duplicateFirst = 0
                    for i in range(1,len(rows)):         # 尋找照片對應csv檔檔名
                        if n == str(rows[i][0]):        #檢查檔銘是否相同
                            first = i
                            if (i+1!=len(rows))and(rows[i][0] == rows[i+1][0])or(rows[i][0] == rows[i-1][0]):  #檢查下一列   一樣為多物件
                                if(rows[i][0]!=rows[i-1][0]):
                                    y = i - 1
                                    duplicateFirst = i      
                                y = y + 1 
                            else:
                                y = first 
                        
                    if(duplicateFirst>0):
                        first = duplicateFirst
                    # 0: filename 1:file_size 2: file_attributes 3: region_count 4: region_id 5: region_shape_attribute 6: region
                    
                    for x in range(first, y+1):
                        rows[x][0] = hueFilename(rows[x][0], pic_count)
                        cv2.rectangle(image, (int(rows[x][4]),int(rows[x][5])), (int(rows[x][6]),int(rows[x][7])), (0,0,255), 2)
                    cv2.imwrite(save_path + pic_name + "_after_" + str(pic_count) + "_hue." + str(extension[len(extension)-1]),image)
            addcount = 0 
            with open(csvFilename, "a", newline='') as wcsvfile: # csv標頭
                writer = csv.writer(wcsvfile)
                for row in rows:
                    if (count!=0)and(addcount==0):            # 不是第一次寫入
                        addcount = addcount + 1
                        continue
                    writer.writerow(row)
                    addcount = addcount + 1
                count = count + 1
#hue("C:\\Users\\D000016264\\Desktop\\python\\","C:\\Users\\D000016264\\Desktop\\python\\save\\",5,-0.5,0.5)
#flip("C:\\Users\\D000016264\\Desktop\\python\\","C:\\Users\\D000016264\\Desktop\\python\\save\\",-1,1)
#shift("C:\\Users\\D000016264\\Desktop\\images\\test\\","C:\\Users\\D000016264\\Desktop\\images\\test\\save\\",3,5,3,5)
#bright("C:\\Users\\D000016264\\Desktop\\python\\data\\test\\","C:\\Users\\D000016264\\Desktop\\python\\data\\test\\save\\",5,25,1.1,1.2)
#rotate("C:\\Users\\D000016264\\Desktop\\python\\data\\test\\","C:\\Users\\D000016264\\Desktop\\python\\data\\test\\save\\",50,230)
#resize("C:\\Users\\D000016264\\Desktop\\python\\","C:\\Users\\D000016264\\Desktop\\python\\save\\",1000,1002,500,502)