from random import shuffle
import glob
import tensorflow as tf
import os
import cv2	# openCV
import numpy as np

#--- Parameters ---#
data_path = "dataset-lfw-a/*.jpg"
shuffle_data = True
tfr_train_filename = "/tmp/train_set.tfrecords"
tfr_test_filename = "/tmp/test_set.tfrecords"


def load_image(addr):
	# reads img data
	img = cv2.imread(addr)
	# converts colors to RBG (loaded as BGR)
	img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
	# stores img as float32
	img = img.astype(np.float32)
	return img

def _int64_feature(value):
	# converts an int64 into a Tensorflow Feature
	return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))

def _bytes_feature(value):
	# converts bytes into a Tensorflow Feature
	return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))

def label_images():
	# get the images' path in a set and stores them alphabetically
	addrs = glob.glob(data_path)
	addrs.sort(key=str.lower)
	
	labels = []
	label = -1

	# labels the images differently if they are from different persons
	for addr in addrs:
		if "0001" in addr:
			label += 1
		labels.append(label)

	# shuffles the addresses & labels
	if shuffle_data:
		s = list(zip(addrs, labels))
		shuffle(s)
		addrs, labels = zip(*s)

	return (labels, addrs)

def get_train_set(dataset):
	train_labels = dataset[0][:int(.7 * len(dataset[0]))]
	train_addrs = dataset[1][:int(.7 * len(dataset[1]))]
	return (train_labels, train_addrs)

def get_test_set(dataset):
	test_labels = dataset[0][int(.7 * len(dataset[0])):]
	test_addrs = dataset[1][int(.7 * len(dataset[1])):]
	return (test_labels, test_addrs)

def generate_tfr_file(filename, dataset, dataset_type):
	dataset_labels = dataset[0]
	dataset_addrs = dataset[1]

	# opens TFRecords file
	writer = tf.python_io.TFRecordWriter(filename)

	for i in range( len(dataset_addrs) ):
		img = load_image(dataset_addrs[i])
		label = dataset_labels[i]
		# create features from the image
		feature = {'train/label': _int64_feature(label), 'train/image': _bytes_feature(tf.compat.as_bytes(img.tostring()))}
		# create an Example protocol buffer
		example = tf.train.Example(features=tf.train.Features(feature=feature))

		# Serialize to string and write on the file
		writer.write(example.SerializeToString())
	writer.close()

if __name__ == "__main__":
	if not os.path.exists(tfr_train_filename):
		with open(tfr_train_filename, 'w'): pass
	if not os.path.exists(tfr_test_filename):
		with open(tfr_test_filename, 'w'): pass

	# obtains the dataset from the images
	full_dataset = label_images()
	
	# generates the TFR file of the train set
	#generate_tfr_file(tfr_train_filename, get_train_set(full_dataset), "train")
	
	# generates the TFR file of the test set
	generate_tfr_file(tfr_test_filename, get_test_set(full_dataset), "test")
	