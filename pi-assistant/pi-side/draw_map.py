import requests
import json

locations = {
	"Schuman Building": 				(52.673168, -8.577775),
	"Kemmy Business School": 			(52.672711, -8.577147),
	"Computer Science Building":		(52.673941, -8.575160),
	"Glucksman Library": 				(52.673457, -8.573127),
	"Foundation Building": 				(52.674232, -8.573147),
	"Engineering Research Building": 	(52.674974, -8.573015),
	"Languages Building": 				(52.675565, -8.573269),
	"Lonsdale Building": 				(52.673634, -8.569123),
	"Schrödinger Building": 			(52.673506, -8.567477),
	"PESS Building": 					(52.674411, -8.567816),
	"Health Sciences Building": 		(52.677731, -8.569194),
	"Main Building": 					(52.673981, -8.572065), 
	"Irish World Academy Building": 	(52.677906, -8.569580) 
}

def get_path_points (origin, destination, mode="walking", key="AIzaSyBuPHU3WxdkYfEeqAurIuR3hOUa8pzTy5Y"):
	url = "https://maps.googleapis.com/maps/api/directions/json?"

	url += "origin={},{}&".format(origin[0], origin[1])
	url += "destination={},{}&".format(destination[0], destination[1])
	url += "mode={}&".format(mode)
	url += "key={}".format(key)
	
	r = requests.get(url).json()
	points = r["routes"][0]["overview_polyline"]["points"]

	return points


def get_static_google_map_url(center=None, zoom=None, img_format="jpeg", img_size=(640,360), scale=2, 
							  markers=[{}, {}], key="AIzaSyBuPHU3WxdkYfEeqAurIuR3hOUa8pzTy5Y"):

	url = "https://maps.googleapis.com/maps/api/staticmap?"

	if center != None:
		url += "center={}&".format(center)

	url += "zoom={}&".format(zoom)  
	url += "format={}&".format(img_format)
	url += "size={}x{}&".format(img_size[0], img_size[1])
	url += "scale={}&".format(scale)

	for m in markers:
		separator_needed = False
		marker = "markers="
		
		try:
			marker += "size:" + str(m["size"])
			separator_needed = True
		except KeyError:
			pass

		try:
			if separator_needed:
				marker += "|"
			marker += "color:" + m["color"]			
			separator_needed = True
		except KeyError:
			marker = marker[:-1]

		try:
			if separator_needed:
				marker += "|"
			marker += "label:" + m["label"]			
			separator_needed = True
		except KeyError:
			marker = marker[:-1]

		try:
			if separator_needed:
				marker += "|"
			marker += str(m["location"][0]) + "," + str(m["location"][1])
		except KeyError:
			marker = marker[:-1]

		url += marker + "&"	

	path_points = get_path_points(origin=markers[0]["location"], destination=markers[1]["location"])
	url += "path=color:red|enc:{}&".format(path_points)

	url += "key={}&".format(key)

	return url


def save_map_image(filename, origin, destination):

	markers = [
	{
		"color": "green",
		"label": "O", 
		"location": origin
	},
	{
		"color": "red",
		"label": "D", 
		"location": destination
	}
	]

	r = requests.get(get_static_google_map_url(markers=markers), stream=True)
	
	if r.status_code == 200:
		with open(filename, 'wb') as f:
			for chunk in r.iter_content(1024):
				f.write(chunk)


#markers = [
#{
#	"color": "green",
#	"label": "O", 
#	"location": locations["Computer Science Building"]
#},
#{
#	"color": "red",
#	"label": "D", 
#	"location": locations["Main Building"]
#}
#]

#print(get_static_google_map_url(markers=markers))
#save_map_image("img.jpg", origin=locations["Schuman Building"], destination=locations["PESS Building"])
#print(get_path_points(origin=locations["Computer Science Building"], destination=locations["Main Building"]))