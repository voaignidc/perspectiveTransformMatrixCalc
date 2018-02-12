#!/usr/bin/python3
# -*- coding: utf-8 -*-
import re
import time
import numpy as np
import cv2

from .fileManage import getExtName

ISOTIMEFORMAT = '%Y_%m_%d_%H_%M_%S'
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
    # print(points)
    return points

def sizeInputToPoint(rawStr):
    noBracketStr = re.sub(r"\(","",rawStr)
    noBracketStr = re.sub(r"\)","",noBracketStr)
    noBracketNoSpaceStr = re.sub(r"\s","",noBracketStr)
    pointsStr = re.split(r"\,", noBracketNoSpaceStr)
    points = np.float32([0, 0])
    i = 0
    for s in pointsStr:
        points[i] = int(s)
        i = i+1
    return points

def getMatrix(srcImgPoints, dstImgPoints):
    """
    获取矩阵
    srcImgPoints 原图中选取的4个点
    dstImgPoints 目标中选取的4个点
    """
    transMat = cv2.getPerspectiveTransform(srcImgPoints, dstImgPoints)
    invMat = np.linalg.inv(transMat.T)
    return transMat, invMat

def invMatTocTypeStr(invMat):
    """把np.float32行驶的数组字符串 格式化成 c语言二维数组形式字符串"""
    cTypeStr="{\n"
    count = 1
    for i in invMat:
        cTypeStr = cTypeStr +"{"
        for j in i:
            cTypeStr = cTypeStr + str('%.5f'%j)
            if count%3 == 0:
                cTypeStr = cTypeStr + "}"
                if count == 9:
                    cTypeStr = cTypeStr + "\n"
                else:
                    cTypeStr = cTypeStr + ",\n"
            else:
                cTypeStr = cTypeStr + ","
            count = count + 1
    cTypeStr = cTypeStr + "};"
    return cTypeStr

def doPerspectTransform(filePath, transMat, size):
    """做透视变换"""
    extName = getExtName(filePath)
    img = cv2.imread(filePath)
    # rows, cols, channels = img.shape
    cols,rows = size
    rstImg = cv2.warpPerspective(img, transMat, (cols, rows))
    now_time = time.strftime(ISOTIMEFORMAT, time.localtime()) # 时间随机数防止浏览器缓存
    fileName = "rstImg" + now_time + extName
    fullFileName = "./app/static/images/" + fileName
    cv2.imwrite(fullFileName, rstImg)
    return fileName



