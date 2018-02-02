#!/usr/bin/python3
# -*- coding: utf-8 -*-
import numpy as np
import cv2
import os

def get_inv_mat(src_p, dst_p):    
    '''
    获取逆矩阵
    src_p 原图中选取的4个点
    dst_p 目标中选取的4个点
    '''                                           
    trans_mat = cv2.getPerspectiveTransform(src_p, dst_p).T
    # print('t',trans_mat)
    
    inv_mat = np.linalg.inv(trans_mat)#逆矩阵
    print('逆矩阵inv=\n',inv_mat,'\n')
    print('取5位精度放在c程序的数组里即可')
    print('----------------------------------') 
    return inv_mat
    
def re_perspect(img_src, img_dst, inv_mat, flags = 'NEAREST'):
    '''
    逆透的两种插值方法的实现
    img_src 原图像
    img_dst 目标图像
    inv_mat 用get_inv_mat函数求得的逆矩阵
    flags 选择用哪个插值方法
    '''
    h = img_src.shape[0]
    w = img_src.shape[1]
    
    h2 = img_dst.shape[0]
    w2 = img_dst.shape[1]

    
    if(flags == 'NEAREST'):#最近邻插值
        for pix_y in range(h2):
            for pix_x in range(w2):
                dst_mat = np.array([pix_x,pix_y,1])
                src_mat = np.dot(dst_mat, inv_mat)

                pix_u = int(src_mat[0]/src_mat[2])
                pix_v = int(src_mat[1]/src_mat[2])
                
                condition = pix_u < w and pix_v < h and pix_u >= 0 and pix_v >= 0      
                if(condition):
                    img_dst[pix_y, pix_x] = img_src[pix_v, pix_u]
                    
    
    if(flags == 'DOUBLE_LINEAR'):#双线性插值
        for pix_y in range(h2):
            for pix_x in range(w2):
                dst_mat = np.array([pix_x,pix_y,1])
                src_mat = np.dot(dst_mat, inv_mat)

                pix_u = src_mat[0]/src_mat[2]
                pix_v = src_mat[1]/src_mat[2]
                                                                      
                pix_u_left = (pix_u.astype(int))
                pix_v_up = (pix_v.astype(int))#无需四舍五入
                
                pix_u_right = pix_u_left + 1
                pix_v_down = pix_v_up + 1
                                
                # print(pix_u_left,pix_u_right)
                # print(pix_v_up,pix_v_down)
                                
                condition = pix_u < w-1 and pix_v < h-1 and pix_u >= 1 and pix_v >= 1    
                if(condition):
                    pix_mat = np.float32([ [ img_src[pix_v_down,pix_u_left],img_src[pix_v_up,pix_u_left] ],
                                           [ img_src[pix_v_down,pix_u_right],img_src[pix_v_up,pix_u_right] ] ])
                              
                    tmp_x_mat = np.float32([pix_u_right - pix_u, pix_u - pix_u_left])
                    tmp_y_mat = np.float32([ [pix_v_up - pix_v],
                                             [pix_v - pix_v_down] ])
                        
                    #[right-x,x-left] * [左下值  左上值  * [up-y
                    #                    右下值  右上值]    y-down]
                    
                    img_dst[pix_y, pix_x] = 255 - np.dot(np.dot(tmp_x_mat, pix_mat), tmp_y_mat)
        
    return 1  


  
class IMAGES(object): 
 
    def __init__(self, fn, wn, color):
    
        self.fn = fn                    
        self.wn = wn #wn, window name
        self.color = color
        
        self.img_color = cv2.imread(fn)
        self.img_gray = cv2.imread(fn, 0)
        self.read_img_color_infs()
        
        self.mouse_x = [0, self.width-1, 0,             self.width-1]
        self.mouse_y = [0, 0           , self.height-1, self.height-1]
        self.point_id = 0 #第几个点 0 1 2 3
               
        cv2.namedWindow(self.wn)
        cv2.setMouseCallback(self.wn, self.mouse_refresh)
        cv2.createTrackbar('p', self.wn, 0, 3, self.bar_refresh)
        
        self.draw_circle_x(0)
        self.draw_circle_x(1)
        self.draw_circle_x(2)
        self.draw_circle_x(3)
    
    def read_img_color_infs(self):   
        self.height = self.img_color.shape[0]
        self.width = self.img_color.shape[1] 
        # print(self.height)
        # print(self.width)
        
    def img_color_refresh(self):
        self.img_color = cv2.imread(self.fn)
        self.draw_circle_x(0)
        self.draw_circle_x(1)
        self.draw_circle_x(2)
        self.draw_circle_x(3)

    def mouse_refresh(self, event, x, y, flags, param):
    
        if event == cv2.EVENT_LBUTTONDOWN:#按下鼠标左键,选取坐标
        
            if x > self.width-1:
                x = self.width-1
            if y > self.height-1:
                y = self.height-1             
            if(x < 0): 
                x = 0
            if(y < 0): 
                y = 0              
            self.mouse_x[self.point_id] = x
            self.mouse_y[self.point_id] = y

            print('第', self.point_id, '个点坐标为:')
            print(self.mouse_x[self.point_id], self.mouse_y[self.point_id])
            self.img_color_refresh()
            self.draw_circle_x(self.point_id)  

        if event == cv2.EVENT_RBUTTONDOWN:#按下鼠标右键,选择控制第几个点 
            if(self.point_id >= 3):
                self.point_id = 0
            else:    
                self.point_id += 1
            self.bar_refresh(self.point_id)
        
        if event == cv2.EVENT_MBUTTONDOWN:#鼠标中键进行逆变换 
            '''注意global''' 
            global srcimg_color_obj, dstimg_color_obj
            
            src_p = np.float32([[srcimg_color_obj.mouse_x[0],srcimg_color_obj.mouse_y[0]],
                                 [srcimg_color_obj.mouse_x[1],srcimg_color_obj.mouse_y[1]],
                                 [srcimg_color_obj.mouse_x[2],srcimg_color_obj.mouse_y[2]],
                                 [srcimg_color_obj.mouse_x[3],srcimg_color_obj.mouse_y[3]]]) 
            
            dst_p = np.float32([[dstimg_color_obj.mouse_x[0],dstimg_color_obj.mouse_y[0]],
                                 [dstimg_color_obj.mouse_x[1],dstimg_color_obj.mouse_y[1]],
                                 [dstimg_color_obj.mouse_x[2],dstimg_color_obj.mouse_y[2]],
                                 [dstimg_color_obj.mouse_x[3],dstimg_color_obj.mouse_y[3]]]) 
                     
            inv_mat = get_inv_mat(src_p, dst_p)
            re_perspect(srcimg_color_obj.img_gray, dstimg_color_obj.img_gray , inv_mat) 
        
    def bar_refresh(self, point_id):   
        cv2.setTrackbarPos('p', self.wn, point_id)
        self.point_id = point_id
        # print('point_id',self.point_id)

    def draw_circle_x(self, point_id):

        r = 5
        line_width = 1 
        
        cv2.circle(self.img_color, (self.mouse_x[point_id], self.mouse_y[point_id]), r, self.color, line_width)
          
        rb_x = int(self.mouse_x[point_id] + (2**0.5)*r//2)
        rb_y = int(self.mouse_y[point_id] + (2**0.5)*r//2)
        lt_x = int(self.mouse_x[point_id] - (2**0.5)*r//2)
        lt_y = int(self.mouse_y[point_id] - (2**0.5)*r//2)
        cv2.line(self.img_color, (lt_x, lt_y), (rb_x, rb_y), self.color, line_width)    
        
        rt_x = int(self.mouse_x[point_id] + (2**0.5)*r//2)
        rt_y = int(self.mouse_y[point_id] - (2**0.5)*r//2)
        lb_x = int(self.mouse_x[point_id] - (2**0.5)*r//2)
        lb_y = int(self.mouse_y[point_id] + (2**0.5)*r//2)
        cv2.line(self.img_color, (rt_x, rt_y), (lb_x, lb_y), self.color, line_width)
   


print('逆透视变换求解逆矩阵程序v1.1')

print('作者:郑默语')

print('是否有原图像?只能是灰度或二值图像(若有,放在./_images文件夹里!)\n若有按y 没有按n')
src_flag = input()
if src_flag == 'y':
    print('输入原图像文件名:(比如123.BMP)')
    fn = os.getcwd() + '\\_images\\'+ input()
    print('原图像文件位于:'+fn)
else:
    print('输入原图像宽:(比如80)')
    input_w = int(input())
    print('输入原图像高:(比如60)')
    input_h = int(input())
    src_img = np.zeros((input_h,input_w), np.uint8)
    fn = os.getcwd() + r'\_images\src_standard.bmp'
    cv2.imwrite(fn, src_img)
    print('生成纯黑原图像文件位于:' + fn)
      
print('----------------------------------')  
  
print('输入目标图像宽:(比如60)')
input_w = int(input())
print('输入目标图像高:(比如60)')
input_h = int(input())
dst_img = np.zeros((input_h,input_w), np.uint8)
fn2 = os.getcwd() + r'\_images\dst_standard.bmp'
cv2.imwrite(fn2, dst_img)
print('生成纯黑目标图像文件位于:' + fn2)

print('----------------------------------') 

print('鼠标左键选坐标点位置,右键切换选择第几个坐标点,中键进行透视变换')
print('坐标点一开始在图片的四个角') 
print('红色坐标的是原图像,蓝色的是目标图像') 

print('----------------------------------') 

wn = 'image1'
wn2 = 'image2'

srcimg_color_obj = IMAGES(fn, wn, (0,0,255))
dstimg_color_obj = IMAGES(fn2, wn2, (255,0,0))
        
while(1):  
    k = cv2.waitKey(1) & 0xFF 
    if k == ord('q'):
        break
 
    cv2.imshow(wn, srcimg_color_obj.img_color)         
    cv2.imshow(wn2, dstimg_color_obj.img_color)
    cv2.imshow('image3', dstimg_color_obj.img_gray)        

cv2.destroyAllWindows() 