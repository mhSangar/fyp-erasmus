from flask import jsonify, request, Response
from app import app, db
from app.models import Student
import numpy as np
import json
import cv2
import base64
import time
from utils import scrape_timetable
from utils import static_google_map as g_map
from utils import face_recognition as fr
from utils import face_detection as fd
import datetime as dt
import os
import logging


@app.route("/")
def index():
	return "FYP: Intelligent Assistant, by Mario Sanchez Garcia (17150868)"

@app.route("/recognise_me", methods=["POST"])
def recognise_student():
	logging.info("Recognising face...")

	full_img_filename = store_image(request=request)
	face_img_filename = None
	
	# detect face from photo
	detected_faces = fd.detect_face(full_img_filename, output_dir=app.config["PI_CAPTURES_FOLDER_PATH"])

	if detected_faces == None:
		student_id = "00000000"
		logging.warning("No faces detected!")
	elif len(detected_faces) > 0:
		if len(detected_faces) > 1:
			logging.warning("Multiple faces detected! First detected face was chosen.") 
		
		face_img_filename = detected_faces[0]
		
		# recognise preprocessed photo
		student_id = fr.recognise_face(face_img_filename)

		logging.info("Student recognised: " + student_id + ".")

	#print("\n" + student_id + "\n")

	# get student name
	student = Student.query.filter_by(id=student_id).first()

	# we delete the images that we are not going to use anymore
	delete_image(full_img_filename)
	for img in detected_faces:
		delete_image(img)

	return jsonify({"student_id": student.id, "student_name": student.name})

@app.route("/next_class", methods=["POST"])
def whats_my_next_class():
	student_id = json.loads(request.data)["student_id"]
	logging.info("Getting next class for " + student_id + "...")

	# we get the week timetable of the student
	week_timetable = scrape_timetable.get_week_timetable("17226163")

	# index representing day of the week (0-> Monday, 1->Tuesday...)
	today = (dt.date.today() - dt.timedelta(2)).weekday()
	now = dt.datetime.now()

	# on sunday there are no classes
	if today < 6: 
		for mod in week_timetable[today]:
			if mod.hours[0] > now.hour - 18:
				logging.info("Next class: " + mod.code + ".")
				return jsonify({"next_class": mod.toJSON()})

	logging.info("The student has no more classes today.")
	return jsonify({"next_class": None})

@app.route("/map", methods=["POST"])
def create_map(origin_building="Computer Science Building"):
	logging.info("Getting map...")
	try:
		origin_building = json.loads(request.data)["origin_building"]
	except KeyError:
		pass

	destination_building = json.loads(request.data)["destination_building"]

	img_as_text = g_map.get_map_image(origin=g_map.locations[origin_building], 
									  destination=g_map.locations[destination_building])

	return jsonify({"map_img": img_as_text})


def store_image(request):
	# get image from request
	img_b64 = str(json.loads(request.data)["image"])

	# decode base64
	img_bytes = base64.b64decode(img_b64)
	# encode to uint8 to create a numpy array
	img_np_array = np.fromstring(img_bytes, np.uint8)
	# decode image
	img = cv2.imdecode(img_np_array, cv2.IMREAD_COLOR)

	# we add the image to the db to obtain the id, so every filename is different
	#image = Image(img="")
	#db.session.add(image)
	#db.session.commit()

	# save image to a file
	filename = "unknown-face.jpg"
	filepath = app.config["PI_CAPTURES_FOLDER_PATH"] + filename
	cv2.imwrite(filepath, img)

	# update filename of the image
	#image.img = app.config["PI_CAPTURES_FOLDER_PATH"] + filename
	#db.session.commit()

	return filepath

def delete_image(filepath):
	is_deleted = False

	if os.path.isfile(filepath):
		os.remove(filepath)
		is_deleted = True

	return is_deleted

#@app.route("/recognise_me/<int:student_id>", methods=["DELETE"])
#def delete_imgs_from_user(student_id):
	
