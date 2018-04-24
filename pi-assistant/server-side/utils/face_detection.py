import numpy as np
import cv2
import os
import argparse

classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

def fd_emp_study (input_dir, detected_matrix):

	sorted_file_list = sorted(os.listdir(input_dir))

	for i, file in enumerate(sorted_file_list):
		# load img in grayscale
		grayscale_img = cv2.imread(os.path.join(input_dir, file), 0)
		# face detection with viola-jones
		faces = classifier.detectMultiScale(grayscale_img, scaleFactor=1.3, minNeighbors=5)
		
		if len(faces) == 0:
			is_detected = False
		else:
			is_detected = True
	
		detected_matrix.append( (file, is_detected) )

#if __name__ == '__main__':
#	parser = argparse.ArgumentParser(add_help=True)
#
#	parser.add_argument('--input-dir', type=str, action='store', default='img/', dest='input_dir')	
#	args = parser.parse_args()
#
#	detected_matrix = []
#	fd_emp_study(args.input_dir, detected_matrix)
#
#	for face in detected_matrix:
#		print(face[0] + ": " + str(face[1]))


all_imgs = True
display_info = True

limits = [100, 500]

basedir = os.path.abspath(os.path.dirname(__file__))

input_dir = os.path.join(basedir, "img/")
_output_dir = os.path.join(basedir, "out/")



def detect_face(img_filepath, output_dir):
	img = cv2.imread(img_filepath)
	grayscale_img = cv2.imread(img_filepath, 0)

	faces = classifier.detectMultiScale(grayscale_img, scaleFactor=1.3, minNeighbors=5)
	
	if len(faces) == 0:
		return None

	face_img_filepaths = []
	counter = 1

	for (x, y, w, h) in faces:
		crop_img = img[y:y+h, x:x+w].copy()

		# skips imgs too small to be a face in front of the camera
		if len(crop_img) < 150 or len(crop_img[0]) < 150:
			continue

		# resize to a standard size the CNN can process
		crop_img = cv2.resize(crop_img, (160, 160))

		img_filename = img_filepath.split("/")[-1]
		detected_face_filepath = os.path.join(output_dir, img_filename.split(".jpg")[0] + "_fd_{0:0>2}.jpg".format(counter))
		
		cv2.imwrite(detected_face_filepath, crop_img)
		face_img_filepaths.append(detected_face_filepath)
		counter += 1

	if len(face_img_filepaths) == 0:
		return None

	return face_img_filepaths

def lfw_detect_face(filepath, class_name):
	img = cv2.imread(filepath)
	grayscale_img = cv2.imread(filepath, 0)

	faces = classifier.detectMultiScale(grayscale_img, scaleFactor=1.3, minNeighbors=5)
	
	if len(faces) == 0:
		return [-1]

	face_imgs = []
	counter = 1

	for (x, y, w, h) in faces:
		crop_img = img[y:y+h, x:x+w].copy()

		# skips imgs too small to be a face in front of the camera
		if len(crop_img) < 100 or len(crop_img[0]) < 100:
			counter -= 1
			continue

		output_dir_for_class = os.path.join(_output_dir, class_name)
		
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

			faces = lfw_detect_face(os.path.join(_input_dir, file), class_name)

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
				faces = lfw_detect_face(os.path.join(_input_dir, file))

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
	