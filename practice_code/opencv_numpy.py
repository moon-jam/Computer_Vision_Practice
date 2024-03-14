import cv2
import numpy as np
import random

img = cv2.imread('colorcolor.jpg')
# print(img.shape)
# # B G R

# img = np.empty((300,300,3), np.uint8)

# for row in range(300):
#     for col in range(img.shape[1]):
#         img[row][col] = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]

img2 = img[700:950, 200:400]

cv2.imshow('img', img)
cv2.imshow('img2', img2)
cv2.waitKey(0)