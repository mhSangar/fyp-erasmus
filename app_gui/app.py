from PIL import Image
from PIL import ImageTk
from scrape_timetable_website import Timetable_Class
import scrape_timetable_website
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font
import os
import base64
import requests
import json
import cv2
import threading

port = 5000
route = "recognise_me"
server_url = "http://localhost:{}/{}".format(port, route)

class FullScreenApp(object):
	def __init__(self, master, **kwargs):
		self.master = master
		self.bg_color = "#eff0f1"
		self.screen_width = master.winfo_screenwidth()
		self.screen_height = master.winfo_screenheight()
		self.frames = {}
		self.gif_frames = [tk.PhotoImage(file="loading_ring.gif", format="gif -index {}".format(i)) for i in range(14)]
		self.response = None
		self.resp_received_flag = tk.BooleanVar()

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

		self.frames["home"] = tk.Frame(container, bg=self.bg_color, width=self.screen_width, 
			height=self.screen_height)
		self.frames["home"].grid(row=0, column=0, sticky="nsew")
		self.create_home_frame()

		#### PREVIEW ####

		self.frames["preview"] = tk.Frame(container, bg=self.bg_color, width=self.screen_width, 
			height=self.screen_height)
		self.frames["preview"].grid(row=0, column=0, sticky="nsew")
		self.create_preview_frame()

		#### SHOW CAPTURE ####

		self.frames["show_capture"] = tk.Frame(container, bg=self.bg_color, width=self.screen_width, 
			height=self.screen_height)
		self.frames["show_capture"].grid(row=0, column=0, sticky="nsew")
		self.create_show_capture_frame()

		#### CONNECTING WITH SERVER ####

		self.frames["connecting_with_server"] = tk.Frame(container, bg=self.bg_color, width=self.screen_width, 
			height=self.screen_height)
		self.frames["connecting_with_server"].grid(row=0, column=0, sticky="nsew")
		self.create_conn_with_server_frame()		

		#1. Comment the 37th and 38th line of your code
		#2. add self.videoLoop() just after the former 38th line
		#3. change the “while not” in line 51 to “if not”
		#4. add this line “self.panel.after(10, self.videoLoop)” to the last of the function videoLoop().

		#### WELCOME STUDENT ####

		self.frames["welcome_student"] = tk.Frame(container, bg=self.bg_color, width=self.screen_width, 
			height=self.screen_height)
		self.frames["welcome_student"].grid(row=0, column=0, sticky="nsew")
		self.create_welcome_student_frame()		

		#### SHOW MAP ####

		self.frames["show_map"] = tk.Frame(container, bg=self.bg_color, width=self.screen_width, 
			height=self.screen_height)
		self.frames["show_map"].grid(row=0, column=0, sticky="nsew")
		self.create_show_map_frame()		

		self.show_frame("home")


	#### CREATING FRAME CONTENTS ####

	def create_home_frame(self):
		title_font = tkinter.font.Font(family="Helvetica", size=35, weight="bold")
		by_font = tkinter.font.Font(family="Helvetica", size=20, weight="bold")
		author_font = tkinter.font.Font(family="Helvetica", size=30, weight="bold")

		centered_canvas = tk.Canvas(self.frames["home"], bg=self.bg_color, highlightthickness=0)
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
			cursor="hand1", padding="0 15 0 15", command=lambda: self.show_frame("show_capture"))
		preview_bt.grid(row=3, column=0, sticky="N")

	def create_preview_frame(self):
		pass

	def create_show_capture_frame(self):
		centered_canvas = tk.Canvas(self.frames["show_capture"], bg=self.bg_color, highlightthickness=0)
		centered_canvas.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=self.screen_width)
		centered_canvas.pack(expand=False)

		img = cv2.imread("placeholder.jpg")
		img = cv2.resize(img, None, fx=0.5, fy=0.5)
		img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
		img = ImageTk.PhotoImage(Image.fromarray(img))

		img_label = ttk.Label(centered_canvas, image=img, background=self.bg_color,
			padding="0 50 0 30")
		img_label.image = img
		img_label.grid(row=0, column=0, sticky="N")

		bt_canvas = tk.Canvas(centered_canvas, bg=self.bg_color, highlightthickness=0)
		bt_canvas.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=self.screen_width)
		bt_canvas.grid(row=1, column=0, sticky="N")

		accept_bt = ttk.Button(bt_canvas, text="Accept this photo", width=50, 
			cursor="hand1", padding="0 15 0 15", command=lambda: self.connect_with_server())
		accept_bt.grid(row=0, column=0, sticky="W")

		blank = ttk.Label(bt_canvas, background=self.bg_color, padding="40 0 40 0")
		blank.grid(row=0, column=2, sticky="W")

		cancel_bt = ttk.Button(bt_canvas, text="Take photo again", width=50, 
			cursor="hand1", padding="0 15 0 15", command=lambda: self.show_frame("show_map"))
		#	cursor="hand1", padding="0 15 0 15", command=lambda: self.show_frame("preview"))
		cancel_bt.grid(row=0, column=3, sticky="W")

	def create_conn_with_server_frame(self):
		label_font = tkinter.font.Font(family="Helvetica", size=13)

		centered_canvas = tk.Canvas(self.frames["connecting_with_server"], bg=self.bg_color, 
			highlightthickness=0)
		centered_canvas.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=self.screen_width)
		centered_canvas.pack(expand=False)

		gif_label = ttk.Label(centered_canvas, background=self.bg_color, image=self.gif_frames[0], 
			padding="0 120 0 40")
		gif_label.grid(row=0, column=0, sticky="N")

		loading_conn_label = ttk.Label(centered_canvas, background=self.bg_color, font=label_font,
			text="Connecting with server...", padding="0 0 0 10")
		loading_conn_label.grid(row=1, column=0, sticky="N")
		
		loading_wait_label = ttk.Label(centered_canvas, background=self.bg_color, font=label_font,
			text="Please, wait.", padding="0 0 0 40")
		loading_wait_label.grid(row=2, column=0, sticky="N")

		hello_user = ttk.Label(centered_canvas, background=self.bg_color, font=label_font,
			text="")
		hello_user.grid(row=3, column=0, sticky="N")

		self.update_label(loading_conn_label, 0)
		self.update_gif(gif_label, 0)

	def create_welcome_student_frame(self):
		self.student_name = ""
		self.next_class = Timetable_Class(code="CS4618", init_hour="00:00", end_hour="00:00", type="", location="CSG027", weeks="Wks:1-13", group=None)

		title_font = tkinter.font.Font(family="Helvetica", size=55, weight="bold")
		text_font = tkinter.font.Font(family="Helvetica", size=12)

		centered_canvas = tk.Canvas(self.frames["welcome_student"], bg=self.bg_color, highlightthickness=0)
		centered_canvas.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=self.screen_width)
		centered_canvas.pack(expand=False)

		welcome_label = ttk.Label(centered_canvas, font=title_font, background=self.bg_color,
			text="Welcome {}!", wraplength=1200, justify="center", padding="20 150 20 20")
		welcome_label.grid(row=0, column=0, sticky="N")

		next_class_name_label = ttk.Label(centered_canvas, font=text_font, background=self.bg_color,
			text="Your next class is {}: {}".format(self.next_class.code, self.next_class.name), padding="20 100 20 20")
		next_class_name_label.grid(row=1, column=0, sticky="N")

		next_class_type_label = ttk.Label(centered_canvas, font=text_font, background=self.bg_color,
			text="Type: {}".format(self.next_class.type), padding="15")
		next_class_type_label.grid(row=2, column=0, sticky="N")

		next_class_location_label = ttk.Label(centered_canvas, font=text_font, background=self.bg_color,
			text="Location: {}".format(self.next_class.location), padding="20 20 20 80")
		next_class_location_label.grid(row=3, column=0, sticky="N")

		show_map_bt = ttk.Button(centered_canvas, text="Show route to the class", width=100, 
			cursor="hand1", padding="0 15 0 15", command=lambda: self.show_frame("show_map"))
		show_map_bt.grid(row=4, column=0, sticky="N")

	def create_show_map_frame(self):
		title_font = tkinter.font.Font(family="Helvetica", size=25, weight="bold")
		
		centered_canvas = tk.Canvas(self.frames["show_map"], bg=self.bg_color, highlightthickness=0)
		centered_canvas.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=self.screen_width)
		centered_canvas.pack(expand=False)

		welcome_label = ttk.Label(centered_canvas, font=title_font, background=self.bg_color,
			text="Your next class is {}: {}".format(self.next_class.code, self.next_class.name), wraplength=1150, justify="center", padding="20 60 20 20")
		welcome_label.grid(row=0, column=0, sticky="N")

		img = cv2.imread("placeholder.jpg")
		img = cv2.resize(img, None, fx=0.5, fy=0.5)
		img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
		img = ImageTk.PhotoImage(Image.fromarray(img))

		img_label = ttk.Label(centered_canvas, image=img, background=self.bg_color,
			padding="0 50 0 0")
		img_label.image = img
		img_label.grid(row=1, column=0, sticky="N")


	#### HELPER FUNCTIONS ####

	def show_frame(self, frame_name):
		self.frames[frame_name].tkraise()

	def exit_app(self, event):
		self.master.quit()

	def send_img(self):
		img_encoded = cv2.imread("img.jpg")
		#_, img_encoded = cv2.imencode(".jpg", rawCapture.array)
		img_as_text = base64.b64encode(img_encoded)

		data = {"image": img_as_text}
		# send req by POST with the img
		try:
			self.response = requests.post(server_url, json=data)
		except requests.exceptions.RequestException:
			self.response = -1
			print("ERROR - Connection error")
			self.master.quit()

	def connect_with_server (self):
		self.show_frame("connecting_with_server")

		# launch thread and wait for response
		threading.Thread(target=self.send_img).start()
		self.wait_for_response()
		self.frames["connecting_with_server"].wait_variable(self.resp_received_flag)

		self.show_frame("welcome_student")

	def get_student_data(self):
		# name and ID from self.response
		pass
	
	def wait_for_response(self):
		if self.response == None:
			self.master.after(1000, self.wait_for_response)
			#print("not yet")
		else:
			self.resp_received_flag.set(True)
			#print("received")

	def update_gif(self, label, index):
		if index == len(self.gif_frames):
			index = 0

		frame = self.gif_frames[index]
		index += 1
		label.configure(image=frame)
		self.master.after(35, self.update_gif, label, index)

	def update_label(self, label, index):
		if index == 0:
			label.configure(text="Connecting with server")
		elif index == 1:
			label.configure(text="Connecting with server.")
		elif index == 2:
			label.configure(text="Connecting with server..")
		else:
			label.configure(text="Connecting with server...")
			index = -1
		
		index += 1

		self.master.after(500, self.update_label, label, index)
		
#### MAIN ####

root = tk.Tk()
app = FullScreenApp(root)

tk.mainloop()