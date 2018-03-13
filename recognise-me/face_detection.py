import numpy as np
import cv2
import os

all_imgs = False
display_info = False

limits = [100, 400]

basedir = os.path.abspath(os.path.dirname(__file__))

input_dir = os.path.join(basedir, "dataset-lfw-a/")
output_dir = os.path.join(basedir, "lfw-a-faces/")

classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

n = len(os.listdir(input_dir))

def detect_face(filepath):
	img = cv2.imread(filepath)
	grayscale_img = cv2.imread(filepath, 0)

	faces = classifier.detectMultiScale(grayscale_img, scaleFactor=1.3, minNeighbors=5)
	
	if len(faces) == 0:
		return [-1]

	face_imgs = []
	counter = 1

	for (x, y, w, h) in faces:
		#cv2.rectangle(img, (x,y), (x+w, y+h), (0, 0, 255), 2)
		crop_img = img[y:y+h, x:x+w].copy()
		f = filepath.split("/")[-1]
		new_f = os.path.join(output_dir, f.split(".jpg")[0] + "_fd_{0:0>2}.jpg".format(counter))
		cv2.imwrite(new_f, crop_img)
		face_imgs.append(new_f)
		counter += 1

	return face_imgs

if __name__ == '__main__':
	x = -1
	multiple = []
	skipped = []

	if all_imgs:
		for file in os.listdir(input_dir):
			x += 1
			faces = detect_face(os.path.join(input_dir, file))
			if len(faces) > 1:
				multiple.append(file.split(".jpg")[0])
			elif faces[0] == -1:
				skipped.append(file.split(".jpg")[0])
			print("\r{}/{}".format(x+1, n), end="", flush=True)
	else:
		for file in os.listdir(input_dir):
			x += 1

			if x < limits[0]:
				continue
			elif x >= limits[0] and x < limits[1]:
				faces = detect_face(os.path.join(input_dir, file))
				if len(faces) > 1:
					multiple.append(file.split(".jpg")[0])
				elif faces[0] == -1:
					skipped.append(file.split(".jpg")[0])
				print("\r{}/{}".format(x+1 - limits[0], limits[1]-limits[0]), end="", flush=True)
			else:
				break

	if display_info:
		if len(multiple) > 0:
			print("\n> More than one face detected in:")
			for i in multiple:
				print("\t", end="")
				print(i)

		if len(skipped) > 0:
			print("\n> No faces detected in:")
			for i in skipped:
				print("\t", end="")
				print(i)
	else:
		print("")
	