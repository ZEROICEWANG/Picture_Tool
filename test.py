import os
import cv2 as cv
import matplotlib.pyplot as plt
img='imgs/00000.jpg'
img=cv.imread(img)
print(img.shape)
part=img[0:235,603:]
plt.imshow(part)
plt.show()
# a='./data/config/asv.gif'
# print(os.path.split(a))

#计算两个特征的相似度
# def get_feature_similarity(feature1,feature2):
    
# 