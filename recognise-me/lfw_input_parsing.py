import os
import numpy as np

class PersonClass():
	def __init__(self, name, img_paths):
		self.name = name
		self.img_paths = img_paths

	def __str__(self):
		return "{}: {} images".format(self.name, len(self.img_paths))

	def __len__(self):
		return len(self.img_paths)		

def parse_dataset(lfw_dir):
	dataset = []

	classes = os.listdir(lfw_dir)
	classes.sort()
	for i in range(len(classes)):
		class_name = classes[i]
		person_folder = os.path.join(lfw_dir, class_name)
		
		img_paths = []

		for img in os.listdir(person_folder):
			img_paths.append(os.path.join(person_folder, img))

		dataset.append(PersonClass(class_name, img_paths))

	return dataset

def split_dataset(dataset, split_ratio=0.7):
	train_set = []
	test_set = []

	for data_class in dataset:
		img_paths = data_class.img_paths
		np.random.shuffle(img_paths)
		
		#CHANGE
		split = int(len(img_paths) * split_ratio)

		if split < 2:
			# not enough images
			continue 

		train_set.append(PersonClass(data_class.name, img_paths[0:split]))
		trest_set.append(PersonClass(data_class.name, img_paths[split:-1]))

	return train_set, test_set