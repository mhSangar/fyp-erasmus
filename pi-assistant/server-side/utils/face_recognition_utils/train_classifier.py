import argparse
import logging
import os
import pickle
import sys
import time
import numpy as np
import tensorflow as tf
from tensorflow.python.platform import gfile
# scitik classifier
from sklearn.svm import SVC

# own file
from utils.face_recognition_utils import lfw_input_parsing

def get_train_test_datasets(input_dir, split_ratio):
	dataset = lfw_input_parsing.parse_dataset(input_dir)
	train_set, test_set = lfw_input_parsing.split_dataset(dataset, split_ratio=split_ratio)
	return train_set, test_set

def load_imgs_labels(dataset, img_size, batch_size, num_epochs, num_threads, random_flip=False, random_brightness=False, random_contrast=False):
	img_paths = []
	label_list = []
	class_names = []

	counter = 0
	
	for data_class in dataset:
		img_paths += data_class.img_paths
		label_list += [counter] * len(data_class.img_paths)
		class_names.append(data_class.name)
		counter += 1

	imgs, labels = lfw_input_parsing.load_data(img_paths, label_list, img_size, batch_size,
												num_epochs, num_threads, shuffle=False, 
												random_flip=random_flip, random_brightness=random_brightness, 
												random_contrast=random_contrast)

	return imgs, labels, class_names

def load_graph_model(model_path):
	model_path_ext = os.path.expanduser(model_path)
	if os.path.isfile(model_path_ext):
		#logging.info("Model filename: {}".format(model_path_ext.split("/")[-1]))
		with gfile.FastGFile(model_path_ext, "rb") as f:
			# create a tf graph
			graph_def = tf.GraphDef()
			# fill it with the data of the previous model
			graph_def.ParseFromString(f.read())
			# use it for tf
			tf.import_graph_def(graph_def, name="")
	else:
		logging.error("Model file is missing. Exiting...")
		sys.exit(-1)

def create_embeddings(embedding_layer, imgs, labels, imgs_placeholder, phase_train_placeholder, sess):
	embeddings_arr = None
	labels_arr = None

	try:
		i = 0
		while True:
			batch_imgs, batch_labels = sess.run([imgs, labels])
			logging.info("Processing iter {}, batch size: {}".format(i, len(batch_imgs)))
			embedding = sess.run(embedding_layer, 
								feed_dict={imgs_placeholder: batch_imgs, phase_train_placeholder: False})

			if embeddings_arr is None:
				embeddings_arr = embedding
			else:
				embeddings_arr = np.concatenate([embeddings_arr, embedding])

			if labels_arr is None:
				labels_arr = batch_labels
			else:
				labels_arr = np.concatenate([labels_arr, batch_labels])	
			
			i += 1
	except tf.errors.OutOfRangeError:
		# finish condition of the while-true loop
		pass		

	return embeddings_arr, labels_arr

def train_and_save_classifier(embeddings_arr, labels_arr, class_names, classifier_filename_out):
	logging.info("Training classifier")
	model = SVC(kernel="linear", probability=True, verbose=False)
	# training
	model.fit(embeddings_arr, labels_arr)

	with open(classifier_filename_out, "wb") as outfile:
		# saving
		pickle.dump((model, class_names), outfile)

	logging.info("Classifier model saved to file: {}".format(classifier_filename_out))

def eval_classifier(embeddings_arr, labels_arr, classifier_filename, is_one_img):
	final_prediction = []

	logging.info("Evaluating classifier on {} images".format(len(embeddings_arr)))

	if not os.path.exists(classifier_filename):
		raise ValueError("Classifier not found, have you trained it first?")

	with open(classifier_filename, "rb") as f:
		model, class_names = pickle.load(f)

		predictions = model.predict_proba(embeddings_arr, )
		best_class_i = np.argmax(predictions, axis=1)
		best_class_prob = predictions[np.arange(len(best_class_i)), best_class_i]

		if is_one_img:
			#print("\n    > Prediction: {} with a {:.2f}%\n".format(class_names[best_class_i[0]], best_class_prob[0]*100))
			final_prediction.append(class_names[best_class_i[0]])
		else:
			for i in range(len(best_class_i)):
				print("{:4d} {}: {:.3f}".format(i, class_names[best_class_i[i]], best_class_prob[i]))
				final_prediction.append(class_names[best_class_i[i]])

			accuracy = np.mean(np.equal(best_class_i, labels_arr))
			print("Accuracy: {:.3f}".format(accuracy))

	return final_prediction

def get_prediction(img_path, model_path, classifier_path, batch_size=128, 
				   num_threads=2, num_epochs=1):
	start = time.time()

	with tf.Session(config=tf.ConfigProto(log_device_placement=False)) as sess:
		class_names = ["Unknown Person"]

		imgs, labels = lfw_input_parsing.load_img(img_path, label=-1, img_size=160, 
													batch_size=batch_size, num_threads=num_threads) 
		
		load_graph_model(model_path)
		
		init_op = tf.group(tf.global_variables_initializer(), tf.local_variables_initializer())
		sess.run(init_op)

		imgs_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
		embedding_layer = tf.get_default_graph().get_tensor_by_name("embeddings:0")
		phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")

		coord = tf.train.Coordinator()
		threads = tf.train.start_queue_runners(coord=coord, sess=sess)

		embeddings_arr, labels_arr = create_embeddings(embedding_layer, imgs, labels, imgs_placeholder, 
														phase_train_placeholder, sess)

		coord.request_stop()
		coord.join(threads)
		#logging.info("Created {} embeddings".format(len(embeddings_arr)))

		prediction = eval_classifier(embeddings_arr, labels_arr, classifier_path, is_one_img=True)[0]

		duration = time.time() - start
		msg = ""
	
		if duration > 3600:
			hours = int(duration // 3600)
			mins = int(duration % 60)
			secs = (duration % 3600) % 60
			msg = "Completed in {:d} hour(s), {:d} minute(s), {:.4f} second(s)".format(hours, mins, secs)
		elif duration > 60:
			mins = int(duration // 60)
			secs = duration % 60
			msg = "Completed in {:d} minute(s), {:.4f} second(s)".format(mins, secs)
		else:
			msg = "Completed in {:.4f} second(s)".format(duration)

		logging.info(msg)

		return prediction

def main(input_dir, model_path, classifier_output_path, batch_size, 
	num_threads, num_epochs=1, split_ratio=0.8, training=True, is_one_img=False):

	start_time = time.time()

	with tf.Session(config=tf.ConfigProto(log_device_placement=False)) as sess:
		if is_one_img:
			class_names = ["Unknown Person"]

			imgs, labels = lfw_input_parsing.load_img(input_dir, label=-1, img_size=160, 
														batch_size=batch_size, num_threads=num_threads) 
		else:
			train_set, test_set = get_train_test_datasets(input_dir, split_ratio)

			if training:
				imgs, labels, class_names = load_imgs_labels(train_set, img_size=160, batch_size=batch_size, 
															num_epochs=num_epochs, num_threads=num_threads, 
															random_flip=True, random_brightness=True, random_contrast=True)
			else:
				imgs, labels, class_names = load_imgs_labels(test_set, img_size=160, batch_size=batch_size, 
															num_epochs=1, num_threads=num_threads)
		load_graph_model(model_path)
		
		init_op = tf.group(tf.global_variables_initializer(), tf.local_variables_initializer())
		sess.run(init_op)

		imgs_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
		embedding_layer = tf.get_default_graph().get_tensor_by_name("embeddings:0")
		phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")

		coord = tf.train.Coordinator()
		threads = tf.train.start_queue_runners(coord=coord, sess=sess)

		embeddings_arr, labels_arr = create_embeddings(embedding_layer, imgs, labels, imgs_placeholder, 
														phase_train_placeholder, sess)

		coord.request_stop()
		coord.join(threads)
		if not is_one_img:
			logging.info("Created {} embeddings".format(len(embeddings_arr)))

		if training and not is_one_img:
			train_and_save_classifier(embeddings_arr, labels_arr, class_names, classifier_output_path)
		else:
			eval_classifier(embeddings_arr, labels_arr, classifier_output_path, is_one_img)

		duration = time.time() - start
		msg = ""
	
		if duration > 3600:
			hours = int(duration // 3600)
			mins = int(duration % 60)
			secs = (duration % 3600) % 60
			msg = "Completed in {:d} hour(s), {:d} minute(s), {:.4f} second(s)".format(hours, mins, secs)
		elif duration > 60:
			mins = int(duration // 60)
			secs = duration % 60
			msg = "Completed in {:d} minute(s), {:.4f} second(s)".format(mins, secs)
		else:
			msg = "Completed in {:.4f} second(s)".format(duration)

		logging.info(msg)

if __name__ == "__main__":
	
	logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s >>> %(message)s", datefmt="%H:%M:%S")

	_input_dir = "selected_out/Who_Dis/unknown-face-003_fd_01.jpg"
	_model_path = "~/model_dir/20170512-110547/20170512-110547.pb"
	_batch_size = 128
	_num_threads = 1
	_num_epochs = 3
	_split_ratio = 0.8
	_classifier_output_path = "svc_classifier.pkl"
	_training = False
	_is_one_img = True

	main(_input_dir, 
		_model_path, 
		_classifier_output_path, 
		_batch_size,
		_num_threads, 
		_num_epochs, 
		_split_ratio, 
		_training,
		_is_one_img)
