import cv2
import numpy as np
from PIL import Image

import matplotlib.pyplot as plt

def maximum_internal_rectangle(mask_path):
    img = cv2.imread(mask_path)  # 读取图像
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 转换为灰度图

    ret, img_bin = cv2.threshold(img_gray, 0, 255, cv2.THRESH_OTSU)  # 应用二值化处理

    contours, _ = cv2.findContours(img_bin, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)  # 查找轮廓

    contour = contours[0].reshape(len(contours[0]), 2)  # 将第一个轮廓重塑为二维数组

    rect = []

    for i in range(len(contour)):  # 遍历轮廓点
        x1, y1 = contour[i]  # 第一个点的坐标
        for j in range(len(contour)):  # 再次遍历轮廓点
            x2, y2 = contour[j]  # 第二个点的坐标
            area = abs(y2 - y1) * abs(x2 - x1)  # 计算矩形的面积
            rect.append(((x1, y1), (x2, y2), area))  # 将矩形的顶点坐标和面积存入列表

    all_rect = sorted(rect, key=lambda x: x[2], reverse=True)  # 按面积从大到小排序所有矩形

    if all_rect:
        best_rect_found = False
        index_rect = 0
        nb_rect = len(all_rect)

        while not best_rect_found and index_rect < nb_rect:  # 遍历所有矩形，寻找符合条件的最大矩形

            rect = all_rect[index_rect]
            (x1, y1) = rect[0]
            (x2, y2) = rect[1]

            valid_rect = True

            x = min(x1, x2)
            while x < max(x1, x2) + 1 and valid_rect:  # 检查矩形的每一列
                if any(img[y1, x]) == 0 or any(img[y2, x]) == 0:  # 如果列上的任意像素为黑色，则矩形无效
                    valid_rect = False
                x += 1

            y = min(y1, y2)
            while y < max(y1, y2) + 1 and valid_rect:  # 检查矩形的每一行
                if any(img[y, x1]) == 0 or any(img[y, x2]) == 0:  # 如果行上的任意像素为黑色，则矩形无效
                    valid_rect = False
                y += 1

            if valid_rect:
                best_rect_found = True  # 找到符合条件的最大矩形

            index_rect += 1

        if best_rect_found:
            # 如果要在灰度图img_gray上画矩形，请用黑色画（0,0,0）
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 3)  # 在原图像上绘制矩形
            cv2.imshow("rec", img)  # 显示结果图像
            cv2.waitKey(0)
        else:
            print("No rectangle fitting into the area")  # 没有找到符合条件的矩形
    else:
        print("No rectangle found")  # 没有找到任何矩形


if __name__ == "__main__":
    path = r'C:\Users\86150\Desktop\hsv\test1.jpg'
    maximum_internal_rectangle(path)