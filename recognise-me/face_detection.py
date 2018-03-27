import numpy as np
import cv2
import os

all_imgs = True
display_info = True

limits = [100, 500]

basedir = os.path.abspath(os.path.dirname(__file__))

input_dir = os.path.join(basedir, "pi_img/")
output_dir = os.path.join(basedir, "selected_out/")

classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

def detect_face(filepath, class_name):
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

		# skips imgs too small to be a face in front of the camera
		if len(crop_img) < 100 or len(crop_img[0]) < 100:
			counter -= 1
			continue

		output_dir_for_class = os.path.join(output_dir, class_name)
		
		if not os.path.exists(output_dir_for_class):
			os.mkdir(output_dir_for_class)

		crop_img = cv2.resize(crop_img, (160, 160))

		f = filepath.split("/")[-1]
		new_f = os.path.join(output_dir_for_class, f.split(".jpg")[0] + "_fd_{0:0>2}.jpg".format(counter))
		
		cv2.imwrite(new_f, crop_img)
		face_imgs.append(new_f)
		counter += 1

	if len(face_imgs) == 0:
		return [-1]

	return face_imgs

def proccess(_input_dir, multiple, skipped):
	x = 0

	for f in os.listdir(_input_dir):
		if ".jpg" not in f:
			continue
		x += 1

	n = x
	x = -1

	if all_imgs:
		for file in os.listdir(_input_dir):
			if ".jpg" not in file:
				continue

			x += 1
			class_name = _input_dir.split("/")[-1]

			faces = detect_face(os.path.join(_input_dir, file), class_name)

			if len(faces) > 1:
				multiple.append(file.split(".jpg")[0])
			elif faces[0] == -1:
				skipped.append(file.split(".jpg")[0])
			print("\r{}: {}/{}".format(class_name, x+1, n), end="", flush=True)
	else:
		for file in os.listdir(_input_dir):
			if ".jpg" not in file:
				continue

			x += 1

			if x < limits[0]:
				continue
			elif x >= limits[0] and x < limits[1]:
				faces = detect_face(os.path.join(_input_dir, file))

				if len(faces) > 1:
					multiple.append(file.split(".jpg")[0])
				elif faces[0] == -1:
					skipped.append(file.split(".jpg")[0])
				print("\r{}/{}".format(x+1 - limits[0], limits[1]-limits[0]), end="", flush=True)
			else:
				break
	return multiple, skipped

if __name__ == '__main__':
	multiple = []
	skipped = []

	for directory in os.listdir(input_dir):
		multiple, skipped = proccess(input_dir + directory, multiple, skipped)
		print("")

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
	