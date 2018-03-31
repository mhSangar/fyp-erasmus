import os
import cv2

img_paths = os.listdir(".")[1:-2]

for f in img_paths:
	img = cv2.imread(f)
	resized = cv2.resize(img, (360, 480))
	cv2.imwrite(f, resized)
