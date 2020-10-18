# -*-coding: utf-8 -*-
import cv2
import numpy as np

def perspective():
    src = np.float32([[40,138], [72,27], [240,27], [280,138]])
    dst = np.float32([[40, 180], [40, 0], [280, 0], [280,180]])
    M = cv2.getPerspectiveTransform(src, dst)
    Minv = cv2.getPerspectiveTransform(dst, src)
    return M,Minv
def warp(img):
    M, Minv = perspective()
    img_size = (320, 180)
    warped = cv2.warpPerspective(img, M, img_size)
    return warped

def dec_lane(mask):
    mask = cv2.resize(mask,dsize=(16,9))
    mask = (mask/255)
    line_point = mask[2]
    list = []
    for i in range(len(line_point) - 1):
        list.append(abs((int(line_point[i + 1]) - int(line_point[i]))))    
    counter = sum(list)
    print('The counter is ：',counter)
    if 6 < counter<20 :
        flag = 1
        print('Decrease lane has been detect ...')
    else:
        flag = 0
    return flag

def rightangle(mask):
    mask = cv2.resize(mask,dsize=(16,9))
    mask = mask/255
    counter = 0
    for i in range(mask.shape[1]):
        single_list = mask[:,i]
        tem_list = []
        for j in range(len(single_list) - 1):
            tem_list.append(abs(int(single_list[j + 1] - single_list[j])))
        counter = sum(tem_list)+counter
    print("The counter is :",counter)
    
    return counter

def sobel(warped,thresh = (30,180)):
    gray = cv2.cvtColor(warped,cv2.COLOR_RGB2GRAY)
    sobel = np.absolute(cv2.Sobel(gray,cv2.CV_64F,1,1))
    scal_sobel = np.uint8(255*sobel/np.max(sobel))
    mask = np.zeros_like(scal_sobel)
    mask[(scal_sobel >=thresh[0]) & (scal_sobel <=thresh[1])] = 1
    mask = mask *255
    
    return mask


if __name__ == '__main__':
    img = cv2.imread('./408.jpg')
    img = cv2.resize(img, dsize=(320, 180))    
    frame = warp(img)
    mask0 = sobel(frame)
    num = dec_lane(mask0)
    #rightangle(mask0)
