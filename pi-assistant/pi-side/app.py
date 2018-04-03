from imutils.video import VideoStream
from PIL import Image
from PIL import ImageTk
import imutils
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font
import os
import base64
import requests
import json
import cv2
import threading
import numpy as np
import time

port = 5000
ip = "192.168.1.104"
server_url = "http://{}:{}".format(ip, port)
imgs_dir = "images/"
degrees = 0

class FullScreenApp(object):
	def __init__(self, master, **kwargs):
		self.master = master
		self.bg_color = "#eff0f1"
		self.screen_width = master.winfo_screenwidth()
		self.screen_height = master.winfo_screenheight()
		self.frames = {}
		self.gif_frames = [tk.PhotoImage(file=imgs_dir + "loading_icon.gif", format="gif -index {}".format(i)) for i in range(14)]
		self.next_class = None
		self.student_id = "00000000"
		self.video_frame = None
		self.vs = VideoStream(usePiCamera=False, resolution=(1280,720)).start()
		#time.sleep(2.0)

		self.is_detected = None
		self.is_recognised = None
		self.has_classes = None

		self.resp_received = tk.StringVar()
		self.stop_video_stream = tk.BooleanVar()

		self.resp_received.set("none")

		#master.geometry("{}x{}+0+0".format(self.screen_width, self.screen_height))
		#master.geometry("{}x{}+0+0".format(800,300))
		master.wm_attributes("-fullscreen", True)
		master.title("Intelligent Assistant with Face Recognition")
		master.bind("<Escape>", self.exit_app)

		container = tk.Frame(master)
		container.pack(expand=True, side="top", fill="both")
		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)

		#### HOME ####

		self.frames["home"] = {}
		self.frames["home"]["frame"] = tk.Frame(container, bg=self.bg_color, width=self.screen_width, 
			height=self.screen_height)
		self.frames["home"]["frame"].grid(row=0, column=0, sticky="nsew")
		self.create_home_frame()

		#### PREVIEW ####

		self.frames["preview"] = {}
		self.frames["preview"]["frame"] = tk.Frame(container, bg=self.bg_color, width=self.screen_width, 
			height=self.screen_height)
		self.frames["preview"]["frame"].grid(row=0, column=0, sticky="nsew")
		self.create_preview_frame()

		#### SHOW CAPTURE ####

		self.frames["show_snap"] = {}
		self.frames["show_snap"]["frame"] = tk.Frame(container, bg=self.bg_color, width=self.screen_width, 
			height=self.screen_height)
		self.frames["show_snap"]["frame"].grid(row=0, column=0, sticky="nsew")
		self.create_show_snap_frame()

		#### CONNECTING WITH SERVER ####

		self.frames["loading"] = {}
		self.frames["loading"]["frame"] = tk.Frame(container, bg=self.bg_color, width=self.screen_width, 
			height=self.screen_height)
		self.frames["loading"]["frame"].grid(row=0, column=0, sticky="nsew")
		self.create_loading_frame()		

		#### WELCOME STUDENT ####

		self.frames["welcome_student"] = {}
		self.frames["welcome_student"]["frame"] = tk.Frame(container, bg=self.bg_color, width=self.screen_width, 
			height=self.screen_height)
		self.frames["welcome_student"]["frame"].grid(row=0, column=0, sticky="nsew")
		self.create_welcome_student_frame()		

		#### SHOW MAP ####

		self.frames["show_map"] = {}
		self.frames["show_map"]["frame"] = tk.Frame(container, bg=self.bg_color, width=self.screen_width, 
			height=self.screen_height)
		self.frames["show_map"]["frame"].grid(row=0, column=0, sticky="nsew")
		self.create_show_map_frame()

		#### NO MORE CLASSES ####

		self.frames["no_more_classes"] = {}
		self.frames["no_more_classes"]["frame"] = tk.Frame(container, bg=self.bg_color, width=self.screen_width, 
			height=self.screen_height)
		self.frames["no_more_classes"]["frame"].grid(row=0, column=0, sticky="nsew")
		self.create_no_more_classes_frame()

		#### ERROR ####

		self.frames["error"] = {}
		self.frames["error"]["frame"] = tk.Frame(container, bg=self.bg_color, width=self.screen_width, 
			height=self.screen_height)
		self.frames["error"]["frame"].grid(row=0, column=0, sticky="nsew")
		self.create_error_frame()

		self.show_frame("home")


	#### CREATING FRAME CONTENTS ####

	def create_home_frame(self):
		title_font = tkinter.font.Font(family="Helvetica", size=35, weight="bold")
		by_font = tkinter.font.Font(family="Helvetica", size=20, weight="bold")
		author_font = tkinter.font.Font(family="Helvetica", size=30, weight="bold")

		centered_canvas = tk.Canvas(self.frames["home"]["frame"], bg=self.bg_color, highlightthickness=0)
		centered_canvas.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=self.screen_width)
		centered_canvas.pack(expand=False)

		title = ttk.Label(centered_canvas, font=title_font, background=self.bg_color,
			text="FYP: Intelligent Assistant with Face Recognition", 
			padding="20 160 20 20")
		title.grid(row=0, column=0, sticky="N")

		by = ttk.Label(centered_canvas, font=by_font, background=self.bg_color,
			text="by", padding="20 120 20 20")
		by.grid(row=1, column=0, sticky="S")

		author = ttk.Label(centered_canvas, font=author_font, background=self.bg_color,
			text="Mario Sánchez García", padding="20 20 20 110")
		author.grid(row=2, column=0, sticky="S")

		preview_bt = ttk.Button(centered_canvas, text="Start Demo", width=100, 
			cursor="hand1", padding="0 15 0 15", command=lambda: self.show_frame("preview"))
		preview_bt.grid(row=3, column=0, sticky="N")

	def create_preview_frame(self):
		centered_canvas = tk.Canvas(self.frames["preview"]["frame"], bg=self.bg_color, highlightthickness=0)
		centered_canvas.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=self.screen_width)
		centered_canvas.pack(expand=False)

		img = cv2.imread(imgs_dir + "placeholder.jpg")
		img = cv2.resize(img, None, fx=0.5, fy=0.5)
		img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
		img = ImageTk.PhotoImage(Image.fromarray(img))

		self.video_stream_label = ttk.Label(centered_canvas, image=None, background=self.bg_color,
			padding="0 50 0 30")
		self.video_stream_label.image = img
		self.video_stream_label.grid(row=0, column=0, sticky="N")

		bt_canvas = tk.Canvas(centered_canvas, bg=self.bg_color, highlightthickness=0)
		bt_canvas.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=self.screen_width)
		bt_canvas.grid(row=1, column=0, sticky="N")

		take_snapshot_bt = ttk.Button(bt_canvas, text="Take snapshot!", width=100, 
			cursor="hand1", padding="0 15 0 15", command=lambda: self.take_snapshot())
		take_snapshot_bt.grid(row=0, column=0, sticky="N")

	def create_show_snap_frame(self):
		centered_canvas = tk.Canvas(self.frames["show_snap"]["frame"], bg=self.bg_color, highlightthickness=0)
		centered_canvas.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=self.screen_width)
		centered_canvas.pack(expand=False)

		img = cv2.imread(imgs_dir + "placeholder.jpg")
		img = cv2.resize(img, None, fx=0.5, fy=0.5)
		img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
		img = ImageTk.PhotoImage(Image.fromarray(img))

		snap_label = ttk.Label(centered_canvas, image=img, background=self.bg_color,
			padding="0 50 0 30")
		snap_label.image = img
		snap_label.grid(row=0, column=0, sticky="N")

		bt_canvas = tk.Canvas(centered_canvas, bg=self.bg_color, highlightthickness=0)
		bt_canvas.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=self.screen_width)
		bt_canvas.grid(row=1, column=0, sticky="N")

		accept_bt = ttk.Button(bt_canvas, text="Accept this photo", width=50, 
			cursor="hand1", padding="0 15 0 15", command=lambda: self.connect_with_server())
		accept_bt.grid(row=0, column=0, sticky="W")

		blank = ttk.Label(bt_canvas, background=self.bg_color, padding="40 0 40 0")
		blank.grid(row=0, column=2, sticky="W")

		cancel_bt = ttk.Button(bt_canvas, text="Take photo again", width=50, 
		#	cursor="hand1", padding="0 15 0 15", command=lambda: self.show_frame("show_map"))
			cursor="hand1", padding="0 15 0 15", command=lambda: self.show_frame("preview"))
		cancel_bt.grid(row=0, column=3, sticky="W")

		self.frames["show_snap"]["contents"] = {
			"snap_label": snap_label
		}

	def create_loading_frame(self):
		label_font = tkinter.font.Font(family="Helvetica", size=13)

		centered_canvas = tk.Canvas(self.frames["loading"]["frame"], bg=self.bg_color, 
			highlightthickness=0)
		centered_canvas.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=self.screen_width)
		centered_canvas.pack(expand=False)

		gif_label = ttk.Label(centered_canvas, background=self.bg_color, image=self.gif_frames[0], 
			padding="0 120 0 40")
		gif_label.grid(row=0, column=0, sticky="N")

		loading_state_label = ttk.Label(centered_canvas, background=self.bg_color, font=label_font,
			text="", padding="0 0 0 10")
		loading_state_label.grid(row=1, column=0, sticky="N")
		
		loading_wait_label = ttk.Label(centered_canvas, background=self.bg_color, font=label_font,
			text="Who are you?", padding="0 0 0 40")
		loading_wait_label.grid(row=2, column=0, sticky="N")

		hello_user = ttk.Label(centered_canvas, background=self.bg_color, font=label_font,
			text="")
		hello_user.grid(row=3, column=0, sticky="N")

		self.update_label(loading_state_label, loading_wait_label)
		self.update_gif(gif_label)

	def create_welcome_student_frame(self):

		title_font = tkinter.font.Font(family="Helvetica", size=55, weight="bold")
		text_font = tkinter.font.Font(family="Helvetica", size=12)

		centered_canvas = tk.Canvas(self.frames["welcome_student"]["frame"], bg=self.bg_color, highlightthickness=0)
		centered_canvas.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=self.screen_width)
		centered_canvas.pack(expand=False)

		welcome_label = ttk.Label(centered_canvas, font=title_font, background=self.bg_color,
			text="Welcome {}!", wraplength=1200, justify="center", padding="20 150 20 20")
		welcome_label.grid(row=0, column=0, sticky="N")

		next_class_name_label = ttk.Label(centered_canvas, font=text_font, background=self.bg_color,
			text="Your next class is {}: {}", padding="20 100 20 20")
		next_class_name_label.grid(row=1, column=0, sticky="N")

		next_class_type_label = ttk.Label(centered_canvas, font=text_font, background=self.bg_color,
			text="Type: {}", padding="15")
		next_class_type_label.grid(row=2, column=0, sticky="N")

		next_class_location_label = ttk.Label(centered_canvas, font=text_font, background=self.bg_color,
			text="Location: {}", padding="20 20 20 80")
		next_class_location_label.grid(row=3, column=0, sticky="N")

		show_map_bt = ttk.Button(centered_canvas, text="Show route to the class", width=100, 
			cursor="hand1", padding="0 15 0 15", command=lambda: self.show_frame("show_map"))
		show_map_bt.grid(row=4, column=0, sticky="N")

		self.frames["welcome_student"]["contents"] = {
			"welcome_label": welcome_label,	
			"next_class_labels": {
				"name": next_class_name_label,
				"type": next_class_type_label,
				"location": next_class_location_label
			}
		}

	def create_show_map_frame(self):
		title_font = tkinter.font.Font(family="Helvetica", size=25, weight="bold")
		
		centered_canvas = tk.Canvas(self.frames["show_map"]["frame"], bg=self.bg_color, highlightthickness=0)
		centered_canvas.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=self.screen_width)
		centered_canvas.pack(expand=False)

		your_class = ttk.Label(centered_canvas, font=title_font, background=self.bg_color,
			text="Your next class is {}: {}", wraplength=1150, justify="center", padding="20 60 20 20")
		your_class.grid(row=0, column=0, sticky="N")

		img = cv2.imread(imgs_dir + "placeholder.jpg")
		img = cv2.resize(img, (940, 540))
		img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
		img = ImageTk.PhotoImage(Image.fromarray(img))

		map_img_label = ttk.Label(centered_canvas, image=img, background=self.bg_color,
			padding="0 50 0 0")
		map_img_label.image = img
		map_img_label.grid(row=1, column=0, sticky="N")

		self.frames["show_map"]["contents"] = {
			"top_label": your_class,
			"map_img_label": map_img_label
		}

	def create_no_more_classes_frame(self):
		title_font = tkinter.font.Font(family="Helvetica", size=55, weight="bold")
		text_font = tkinter.font.Font(family="Helvetica", size=20)

		centered_canvas = tk.Canvas(self.frames["no_more_classes"]["frame"], bg=self.bg_color, highlightthickness=0)
		centered_canvas.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=self.screen_width)
		centered_canvas.pack(expand=False)

		welcome_label = ttk.Label(centered_canvas, font=title_font, background=self.bg_color,
			text="Welcome {}!", wraplength=1200, justify="center", padding="20 150 20 20")
		welcome_label.grid(row=0, column=0, sticky="N")

		next_class_name_label = ttk.Label(centered_canvas, font=text_font, background=self.bg_color,
			text="You don't have any more classes today!", padding="20 100 20 20")
		next_class_name_label.grid(row=1, column=0, sticky="N")

		self.frames["no_more_classes"]["contents"] = {
			"welcome_label": welcome_label
		}

	def create_error_frame(self):
		title_font = tkinter.font.Font(family="Helvetica", size=30, weight="bold")

		centered_canvas = tk.Canvas(self.frames["error"]["frame"], bg=self.bg_color, highlightthickness=0)
		centered_canvas.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=self.screen_width)
		centered_canvas.pack(expand=False)

		img = cv2.imread(imgs_dir + "red_cross.png", cv2.IMREAD_UNCHANGED)
		img = cv2.resize(img, (300, 300))
		img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA)
		img = ImageTk.PhotoImage(Image.fromarray(img))

		red_cross_img = ttk.Label(centered_canvas, background=self.bg_color, image=img, 
			padding="0 120 0 40")
		red_cross_img.image = img
		red_cross_img.grid(row=0, column=0, sticky="N")

		error_label = ttk.Label(centered_canvas, font=title_font, background=self.bg_color,
			text="<error message>", wraplength=1200, justify="center", padding="20 50 20 20")
		error_label.grid(row=1, column=0, sticky="N")

		self.frames["error"]["contents"] = {
			"error_label": error_label
		}

	#### HELPER FUNCTIONS ####

	def show_frame(self, frame_name):
		if frame_name == "preview":
			self.stop_video_stream.set(False)
			self.video_stream_loop()
			
		self.frames[frame_name]["frame"].tkraise()

	def exit_app(self, event=None):
		# stop videostream from camera
		self.vs.stop()
		# leave it some time to stop
		time.sleep(0.1)
		# exit
		self.master.quit()

	def take_snapshot(self):
		self.stop_video_stream.set(True)
		
		img = imutils.rotate(self.video_frame, degrees)
		img = cv2.flip(img, 1)
		img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
		img = ImageTk.PhotoImage(Image.fromarray(img))

		self.frames["show_snap"]["contents"]["snap_label"]["image"] = img
		self.frames["show_snap"]["contents"]["snap_label"].image = img

		self.show_frame("show_snap")

	def video_stream_loop(self):
		if not self.stop_video_stream.get():
			self.video_frame = self.vs.read()
			#self.video_frame = imutils.resize(self.video_frame, width=500)
			
			next_frame = imutils.rotate(self.video_frame, degrees)
			next_frame = cv2.flip(next_frame, 1)
			next_frame = cv2.cvtColor(next_frame, cv2.COLOR_BGR2RGB)
			next_frame = Image.fromarray(next_frame)
			next_frame = ImageTk.PhotoImage(next_frame)

			self.video_stream_label["image"] = next_frame
			self.video_stream_label.image = next_frame

			self.master.after(10, self.video_stream_loop)

	def refresh_welcome_frame(self):
		contents = self.frames["welcome_student"]["contents"]

		contents["welcome_label"]["text"] = \
			"Welcome {}!".format(self.student_name)
		contents["next_class_labels"]["name"]["text"] = \
			"Your next class is {}: {}".format(self.next_class["code"], self.next_class["name"])
		contents["next_class_labels"]["type"]["text"] = \
			"Type: {}".format(self.next_class["type"])
		contents["next_class_labels"]["location"]["text"] = \
			"Location: {}".format(self.next_class["location"])	

	def refresh_map_frame(self):
		contents = self.frames["show_map"]["contents"]

		contents["top_label"]["text"] = \
			"Your next class is {}: {}".format(self.next_class["code"], self.next_class["name"])

		map_img = cv2.imread(imgs_dir + "map.jpg")
		map_img = cv2.cvtColor(map_img, cv2.COLOR_BGR2RGB)
		map_img = ImageTk.PhotoImage(Image.fromarray(map_img))
			
		contents["map_img_label"]["image"] = map_img
		contents["map_img_label"].image = map_img
		pass	

	def refresh_no_more_classes_frame(self):
		contents = self.frames["no_more_classes"]["contents"]

		contents["welcome_label"]["text"] = \
			"Welcome {}!".format(self.student_name)
		
	def refresh_error_frame(self, error_code):
		contents = self.frames["error"]["contents"]

		if error_code == 0:
			contents["error_label"]["text"] = \
				"Sorry, no face could be detected in the photo."
		
		elif error_code == 1:
			contents["error_label"]["text"] = \
				"Sorry, you were not recognised as a student of the University of Limerick"
		
		else:
			contents["error_label"]["text"] = "Unexpected error."
		
	def recognise_student(self):
		img = cv2.imread(imgs_dir + "snap.jpg")
		_, img_encoded = cv2.imencode(".jpg", img)
		img_as_text = base64.b64encode(img_encoded).decode("ascii")

		data = {"image": img_as_text}
	
		try:
			r = requests.post(server_url + "/recognise_me", json=data)

			self.student_id = json.loads(r.text)["student_id"]
			self.student_name = json.loads(r.text)["student_name"]
			self.is_detected = json.loads(r.text)["is_detected"]
			self.is_recognised = json.loads(r.text)["is_recognised"]
			
			self.resp_received.set("recognition")

		except requests.exceptions.RequestException:
			print("[ERROR] - Connection error. Check if the server is running and the introduced IP is correct.")
			self.resp_received.set("conn_error")
			self.master.quit()

	def get_student_class(self):
		data = {
			"student_id": self.student_id
		}

		try:
			r = requests.post(server_url + "/next_class", json=data)

			next_class_str = json.loads(r.text)["next_class"]

			if next_class_str == None:
				self.has_classes = False
			else:
				self.has_classes = True
				self.next_class = json.loads(next_class_str)

			
			self.resp_received.set("next_class")

		except requests.exceptions.RequestException:
			print("[ERROR] - Connection error. Check if the server is running and the introduced IP is correct.")
			self.resp_received.set("conn_error")
			self.master.quit()

	def get_map(self):
		data = {
			"destination_building": "Foundation Building"
		}

		try:
			r = requests.post(server_url + "/map", json=data)

			# map_img_as_text
			map_img = json.loads(r.text)["map_img"]
			# map_img_bytes
			map_img = base64.b64decode(map_img)
			# map_img_np_array
			map_img = np.fromstring(map_img, np.uint8)
			# map_img_cv2_bgr
			map_img = cv2.imdecode(map_img, cv2.IMREAD_COLOR)
			map_img = cv2.resize(map_img, (940, 540))

			cv2.imwrite(imgs_dir + "map.jpg", map_img)
			
			self.resp_received.set("map")

		except requests.exceptions.RequestException:
			print("[ERROR] - Connection error. Check if the server is running and the introduced IP is correct.")
			self.resp_received.set("conn_error")
			self.master.quit()
	
	def connect_with_server (self):
		self.show_frame("loading")

		snap = imutils.rotate(self.video_frame, degrees)
		snap = cv2.flip(snap, 1)
		cv2.imwrite(imgs_dir + "snap.jpg", snap)

		# recognise student and get ID
		self.current_side_thread = threading.Thread(target=self.recognise_student)
		self.current_side_thread.start()
		self.frames["loading"]["frame"].wait_variable(self.resp_received)

		if self.resp_received.get() == "conn_error":
			self.exit_app()

		# face detected and student recognised
		if self.is_detected and self.is_recognised:
			# get student next class
			self.current_side_thread = threading.Thread(target=self.get_student_class)
			self.current_side_thread.start()
			self.frames["loading"]["frame"].wait_variable(self.resp_received)

			if self.resp_received.get() == "conn_error":
				self.exit_app()

			if self.has_classes:
				self.refresh_welcome_frame()

				# get the map showing the path to next class
				self.current_side_thread = threading.Thread(target=self.get_map)
				self.current_side_thread.start()
				self.frames["loading"]["frame"].wait_variable(self.resp_received)

				if self.resp_received.get() == "conn_error":
					self.exit_app()

				self.refresh_map_frame()

				self.show_frame("welcome_student")
	
			else:	
				self.refresh_no_more_classes_frame()
				self.show_frame("no_more_classes")
			
		# face detected but student not recognised
		elif self.is_detected and not self.is_recognised:
			self.refresh_error_frame(error_code=1)
			self.show_frame("error")

		# face not detected
		else:
			self.refresh_error_frame(error_code=0)
			self.show_frame("error")

	def update_gif(self, label, index=0):
		if index == len(self.gif_frames):
			index = 0

		frame = self.gif_frames[index]
		index += 1
		label.configure(image=frame)
		self.master.after(35, self.update_gif, label, index)

	def update_label(self, label_status, label_wait, index=0):
		text = ""
		if self.resp_received.get() == "none":
			text = "Recognising your face"
		elif self.resp_received.get() == "recognition":
			text = "Getting your next class"
			label_wait["text"] = "Almost finished!"
		elif self.resp_received.get() == "next_class":
			text = "Drawing map"
			#label_wait["text"] = "Please, wait."

		if index == 0:
			label_status["text"] = text + ""
		elif index == 1:
			label_status["text"] = text + "."
		elif index == 2:
			label_status["text"] = text + ".."
		else:
			label_status["text"] = text + "..."
			index = -1
		
		index += 1

		self.master.after(500, self.update_label, label_status, label_wait, index)
		
#### MAIN ####

root = tk.Tk()
app = FullScreenApp(root)

tk.mainloop()
