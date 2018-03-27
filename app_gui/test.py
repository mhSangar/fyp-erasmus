from PIL import Image
import tkinter as tk

root = tk.Tk()

img = Image.open("loading_ring.gif")
counter = 0
#frames = [tk.PhotoImage(file='loading.gif',format = 'gif -index %i' %(i)) for i in range(139)]
#print("Frames: {}".format(len(frames)))

try:
	while 1:
		img.seek(img.tell() + 1)
		counter += 1
except EOFError:
	print("Frames: {}".format(counter))


