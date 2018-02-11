#!/usr/bin/python3
# -*- coding: utf-8 -*-
import re
import numpy as np
import cv2

"""
公式:
src_img   =  dst_img  *  inv_mat_reperspect
原图像    =  目标图像  *  透视变换的逆矩阵
[u, v, m] = [x, y, 1] * ([a00  a01  a02
                          a10  a11  a12
                          a20  a21  a22])
"""

def coordInputToPoint(rawStr):
    """把html里 srcImgCoordInput控件里的字符串内容 转为 4行2列的数组"""
    noBracketStr = re.sub(r"\(","",rawStr)
    noBracketStr = re.sub(r"\)","",noBracketStr)
    noBracketNoSpaceStr = re.sub(r"\s","",noBracketStr)
    pointsStr = re.split(r"\,|\;", noBracketNoSpaceStr)

    points = np.float32([0,0,0,0,0,0,0,0])
    i = 0
    for s in pointsStr:
        points[i] = int(s)
        i = i+1
    points = points.reshape(4,2)
    print(points)
    return points


def getMatrix(srcImgPoints, dstImgPoints):
    """
    获取矩阵
    srcImgPoints 原图中选取的4个点
    dstImgPoints 目标中选取的4个点
    """
    transMat = cv2.getPerspectiveTransform(srcImgPoints, dstImgPoints).T
    invMat = np.linalg.inv(transMat)
    print('矩阵invMat=\n',invMat,'\n')
    return invMat

def savePerspectImg():
    pass


