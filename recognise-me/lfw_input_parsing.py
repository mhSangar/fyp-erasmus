import os
import numpy as np
import tensorflow as tf
from tensorflow.python.framework import ops

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

def split_dataset(dataset, split_ratio=0.8):
	train_set = []
	test_set = []

	for data_class in dataset:
		img_paths = data_class.img_paths
		n = len(img_paths)

		if n < 2:
			# not enough images
			continue 

		np.random.shuffle(img_paths)
		split = int(n * split_ratio)

		train_set.append(PersonClass(data_class.name, img_paths[0:split]))
		test_set.append(PersonClass(data_class.name, img_paths[split:n]))

	return train_set, test_set

def read_img (tf_tensor):
	label = tf_tensor[1]
	contents = tf.read_file(tf_tensor[0])
	
	decoded_img = tf.image.decode_jpeg(contents, channels=3)

	return decoded_img, label


def load_data (img_paths, label_list, img_size, batch_size, num_epochs, num_threads, 
				shuffle, random_flip, random_brightness, random_contrast):
	
	imgs = ops.convert_to_tensor(img_paths, dtype=tf.string)
	labels = ops.convert_to_tensor(label_list, dtype=tf.int32)

	input_tf_queue = tf.train.slice_input_producer((imgs, labels), num_epochs=num_epochs,
		shuffle=shuffle, )

	imgs_labels = []

	for _ in range(num_threads):
		# load the tensor
		tf_tensor = input_tf_queue
		#print("\n")
		#print(tf_tensor)
		#print("\n")
		img, label = read_img(tf_tensor=tf_tensor)
		# random crop of the img (without croping a dimension of RGB, 3)
		img = tf.random_crop(img, size=[img_size, img_size, 3])
		# set the shape specifically for the standardization, 3Dim
		img.set_shape((img_size, img_size, 3))
		# scales img to have zero mean and unit norm.
		img = tf.image.per_image_standardization(img)

		if random_flip:
			img = tf.image.random_flip_left_right(img)

		if random_brightness:
			img = tf.image.random_brightness(img, max_delta=0.3)

		if random_contrast:
			img = tf.image.random_contrast(img, lower=0.2, upper=1.8)

		imgs_labels.append([img, label])

	# capacity = max elements in queue 
	img_batch, label_batch = tf.train.batch_join(imgs_labels, 
												batch_size=batch_size,
												capacity=4*num_threads, 
												enqueue_many=False,
												allow_smaller_final_batch=True)

	return img_batch, label_batch


#def filter_dataset (dataset, min_imgs_per_class=6)
#def get_image_paths_and_labels(dataset)
