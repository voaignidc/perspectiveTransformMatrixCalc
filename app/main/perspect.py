#!/usr/bin/python3
# -*- coding: utf-8 -*-
import re
import numpy as np
import cv2

def coordInputToPoint(rawStr):
    """把html里 srcImgCoordInput控件里的字符串内容 转为 4行2列的数组"""
    noBracketStr = re.sub(r"\(","",rawStr)
    noBracketStr = re.sub(r"\)","",noBracketStr)
    noBracketNoSpaceStr = re.sub(r"\s","",noBracketStr)
    pointsStr = re.split(r"\,|\;", noBracketNoSpaceStr)

    points = np.zeros((8,))
    i = 0
    for s in pointsStr:
        points[i] = int(s)
        i = i+1
    points = points.reshape(4,2)
    return points


def getMatrix(src_p, dst_p):
    """
    获取矩阵
    src_p 原图中选取的4个点
    dst_p 目标中选取的4个点
    """
    trans_mat = cv2.getPerspectiveTransform(src_p, dst_p).T
    # print('t',trans_mat)
    
    inv_mat = np.linalg.inv(trans_mat) # 矩阵
    print('逆矩阵inv=\n',inv_mat,'\n')
    print('取5位精度放在c程序的数组里即可')
    print('----------------------------------') 
    return inv_mat
    
def perspectTransform(img_src, img_dst, inv_mat, flags = 'NEAREST'):
    """
    透视变换的两种插值方法的实现
    img_src 原图像
    img_dst 目标图像
    inv_mat 用get_inv_mat函数求得的逆矩阵
    flags 选择用哪个插值方法
    """
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
