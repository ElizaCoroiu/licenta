import cv2 as cv
import numpy as np

img_rgb = cv.imread('images/mary.jpg')
cv.imshow('template', img_rgb)

img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
template = cv.imread('notes/quarter.png', 0)
cv.imshow('template', template)

w, h = template.shape[::-1]
res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
threshold = 0.7
loc = np.where(res >= threshold)

print(loc)
for pt in zip(loc[1], loc[0]):
    print(pt)
    cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

cv.imwrite('res.png', img_rgb)
result = cv.imread('res.png', 0)
cv.imshow('result', result)

cv.waitKey()
