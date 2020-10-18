# -*- coding:utf - 8 -*-
import cv2
import numpy as np
from lane_detection import Polyfit
import time
from time import sleep
# from decraselane import dec_lane
# from light_recg import recongise
# from corner_det import corner_det
# from light1 import main
cur_mode = 'z'
last_mode = 'z'

def perspective():
    src = np.float32([[32,101], [59,13], [252,13], [288,101]])
    dst = np.float32([[32, 180], [32, 0], [288, 0], [288,180]])

    M = cv2.getPerspectiveTransform(src, dst)
    Minv = cv2.getPerspectiveTransform(dst, src)
    return M,Minv

def warp(img):
    M,Minv = perspective()
    img_size = (320, 180)
    warped = cv2.warpPerspective(img, M, img_size) 
    #cv2.imshow('warp',warped)
##    cv2.waitKey(1)
    return warped
def draw(img, warped, left_fit, right_fit,para=256,meter = 343):#para shi chedao xian kuandu de xiangsu geshu 
    M,Minv = perspective()
    warp_zero = np.zeros_like(warped).astype(np.uint8)
    color_warp = np.dstack((warp_zero, warp_zero, warp_zero))
    # cv2.imshow("color",color_warp)
    plot_y = np.linspace(0, warped.shape[0] - 1, img.shape[0])
    if left_fit !='None':        
        left_fit_x = left_fit[0]*plot_y**2 + left_fit[1]*plot_y + left_fit[2]
        right_fit_x = left_fit_x + para
        #right_fit_x = right_fit[0]*plot_y**2 + right_fit[1]*plot_y + right_fit[2]
        middle_fit_x = (left_fit_x+right_fit_x)/2
        y_axis = warped.shape[0]-2
        point_x = left_fit[0]*y_axis**2 + left_fit[1]*y_axis + left_fit[2]
        left = left_fit[0]*y_axis**2 + left_fit[1]*y_axis + left_fit[2]
        #right = right_fit[0]*y_axis**2 + right_fit[1]*y_axis + right_fit[2]
        right = left + para
        k1 = 2 * left_fit[0]*y_axis + left_fit[1]
        k2 = 2 * left_fit[0]*(y_axis-30) + left_fit[1]
        k_error = round(k1 - k2,2)        
        lane_center = (left+right)/2
        img_center = warped.shape[1]/2
        offset = round((img_center -lane_center)*meter/para,2)
        dy = 2*left_fit[0]*147 + left_fit[1]
        ddy = 2*left_fit[0]
        R = ((1+dy**2)**(3/2))/ddy*meter/para
        pts_left = np.array([np.transpose(np.vstack([left_fit_x, plot_y]))])
        pts_right = np.array([np.flipud(np.transpose(np.vstack([right_fit_x, plot_y])))])
        pts_middle = np.array([np.flipud(np.transpose(np.vstack([middle_fit_x, plot_y])))])
        PTS =np.hstack(pts_middle)
        pts = np.hstack((pts_left, pts_right))
        try:
            cv2.polylines(color_warp,np.int_([PTS]),isClosed=False,color=(255,150,0),thickness=8)
            cv2.polylines(color_warp, np.int_([pts]), isClosed=False, color=(0, 0,255),thickness=3)
        except:
            pass
        newwarp = cv2.warpPerspective(color_warp, Minv, (img.shape[1], img.shape[0]))
        print(img.shape,newwarp.shape,'/./././')
        result = cv2.addWeighted(img, 1, newwarp, 0.3, 0)
        try:
            cv2.putText(result, str('offset:') + str(round(offset, 2)), (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(255, 0, 5), 1)
        except:
            pass
    else:
        k_error = "None"
        offset = 'None'
        result = img
        R = 10000
        '''
        #right_fit_x = right_fit[0]*plot_y**2 + right_fit[1]*plot_y + right_fit[2]
        right_fit_x = left_fit_x + para
        middle_fit_x = (left_fit_x+right_fit_x)/2
        y_axis = warped.shape[0]/2
        left = left_fit[0]*y_axis**2 + left_fit[1]*y_axis + left_fit[2]
        right = left+para
        lane_center = (left+right)/2
        img_center = warped.shape[1]/2
        offset = round((img_center -lane_center)*meter/para,2)
        dy = 2*left_fit[0]*90 + left_fit[1]#147shi jisuan zhongxindian pianyidian de yzuobiao 
        ddy = 2*left_fit[0]
        R = ((1+dy**2)**(3/2))/ddy*meter/para          
        pts_left = np.array([np.transpose(np.vstack([left_fit_x, plot_y]))])
        pts_right = np.array([np.flipud(np.transpose(np.vstack([right_fit_x, plot_y])))])
        pts_middle = np.array([np.flipud(np.transpose(np.vstack([middle_fit_x, plot_y])))])
        PTS =np.hstack(pts_middle)
        pts = np.hstack((pts_left, pts_right))
        try:
            #cv2.fillPoly(color_warp, np.int_([pts]), (0, 255, 0),)
            cv2.polylines(color_warp,np.int_([PTS]),isClosed=False,color=(255,150,0),thickness=8)
            cv2.polylines(color_warp, np.int_([pts]), isClosed=False, color=(0, 0,255),thickness=3)
            # cv2.imwrite("./lane_persp.jpg")
            # cv2.imshow('colormap',color_warp)
        except:
            pass
        # cv2.imwrite("./draw_lane.jpg",color_warp)
        newwarp = cv2.warpPerspective(color_warp, Minv, (img.shape[1], img.shape[0]))
        result = cv2.addWeighted(img, 1, newwarp, 0.3, 0)
        try:
            #cv2.putText(result, str('Radius:') + str(round(R, 2)), (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(255, 0, 5), 1)
            cv2.putText(result, str('offset:') + str(round(offset, 2)), (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(255, 0, 5), 1)
            pass
        except:
            pass 
            '''
    return result,offset,R,k_error

def hsv(warped):
    lower_black = np.array([0,0,0])
    upper_black = np.array([180,255,70])
    hsv = cv2.cvtColor(warped, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_black, upper_black)
    return mask

def sobel(warped,thresh = (30,180)):
    gray = cv2.cvtColor(warped,cv2.COLOR_RGB2GRAY)
    sobel = np.absolute(cv2.Sobel(gray,cv2.CV_64F,1,0))
    scal_sobel = np.uint8(255*sobel/np.max(sobel))
    mask = np.zeros_like(scal_sobel)
    mask[(scal_sobel >=thresh[0]) & (scal_sobel <=thresh[1])] = 1
    mask = mask *255    
    return mask
def canny(warped,low,high):
    gray = cv2.cvtColor(warped,cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray,(3,3),0)
    canny = cv2.Canny(gray,low,high)
    mask = canny * 255
    return mask

        
def auto_lane(img):
    polyfit = Polyfit()
    img = cv2.resize(img,dsize=(320,180))
    
    #light recongise
    GreenLight,RedLight,SpeedLimit,HireSign = recongise(img)
    GreenLight = main(img)
    frame = warp(img)
    mask = hsv(frame)
    # dec_flag = dec_lane(mask)
        
    #mask = canny(frame,50,150)
    #mask = cv2.GaussianBlur(frame,(5,5),0)    
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(2,2))
    mask = cv2.erode(mask,kernel)
    mask = cv2.dilate(mask,kernel)           
    cv2.imshow('mask',mask)
    cv2.waitKey(1)
    try:        
        left_fit, right_fit, vars = polyfit.poly_fit_skip(mask)
        if left_fit =='None'  and right_fit == 'None':
            result,offset,Radius,k_error= img,'None',10000,0
##            cv2.imshow('re', cv2.resize(img, dsize=(640, 320)))
##            cv2.waitKey(1)
        elif left_fit !='None' and right_fit == 'None' or left_fit !='None' and right_fit != 'None' :
            result,offset,Radius ,k_error= draw(img, mask, left_fit, right_fit)
            
##            cv2.imshow('re',cv2.resize(result,dsize=(640,320)))
            cv2.waitKey(1)            
        else:
            result,offset,Radius,k_error = img,0,10000,0

    except:
        result,offset,Radius,k_error = img,0,10000,0
    '''offset --------------------'''
    '''--------------------------lanetype--------------------------'''
    '''zhixian:1..wandao:2...zhijiaowan: 3'''
    if  offset == 'None':
        offset = 'None'
    else:
        offset = offset
    if abs(k_error) < 0.06:
        cur_mode = 1 #wandao
    elif abs(k_error)>=0.06:
        cur_mode = 2 #zhidao
    elif k_error == 'None':
        cur_mode = last_mode#keeping
    
    '''cornerflage'''
    corner_flag = corner_det(mask,img)
    if corner_flag == 0:
        pass
    if corner_flag == 1:
        cur_mode = 3  
    last_mode = cur_mode
    Lane_type = cur_mode
    
    '''-----------SpeedLimit----------'''
    SpeedLimit = 0
    '''-----------RedLight------------'''
    RedLight = 0
    '''-----------GreenLight----------'''
    GreenLight = 0
    '''-----------HireSign------------'''
    HireSign = 0
    '''-----------StopSign------------'''
    StopSign = 0
    cv2.imshow('result',result)
    cv2.waitKey(1)
    return result,offset,Radius,Lane_type,SpeedLimit,RedLight,GreenLight,HireSign,StopSign


if __name__ == "__main__":    
     polyfit = Polyfit()
     original_video = './test4.avi'
     cap = cv2.VideoCapture(original_video)
     n = 0
     while (1):
         n = n+1
         ret,img = cap.read()
         #cv2.imwrite('./tst3/' + str(n) + '.jpg',img)
         start = time.time()
##         cv2.imshow('01',img)
##         cv2.waitKey(1)
         result, offset, Radius,_,_,_,_,_,_ = auto_lane(img)
         print('Time per px :',time.time() - start)
         print(offset,Radius)
'''
    polyfit = Polyfit()
    img = cv2.imread("./278.jpg")
    result, offset, Radius = auto_lane(img)
    print offset,Radius
'''
            
