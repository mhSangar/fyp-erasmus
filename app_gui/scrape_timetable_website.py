from bs4 import BeautifulSoup as bs 
import requests
import re

_student_id = "17226163"

building_dict = {
	"Schuman Building": ("SG", "S1", "S2"),
	"Kemmy Business School": ("KBG", "KG1", "KG2", "KG3"),
	"Computer Science Building": ("CSG", "CS1", "CS2", "CS3"),
	"Glucksman Library": ("GLG", "GL0", "GL1", "GL2"),
	"Foundation Building": ("FB", "FG", "F1", "F2"),
	"Engineering Research Building": ("ERB", "ER0", "ER1", "ER2"),
	"Languages Building": ("LCB", "LC0", "LC1", "LC2"),
	"Lonsdale Building": ("LB", "L0", "L1", "L2"),
	"Schrödinger Building": ("SR1", "SR2", "SR3"),
	"PESS Building": ("PG", "PM", "P1", "P2"),
	"Health Sciences Building": ("HSG", "HS1", "HS2", "HS3"),
	"Main Building": 
		(
			"A0", "AM", "A1", "A2", "A3", 
			"B0", "BM", "B1", "B2", "B3", 
			"CG", "C0", "CM", "C1", "C2", 
			"DG", "D0", "DM", "D1", "D2", 
			"EG", "E0", "EM", "E1", "E2", 
		),
	"Irish World Academy Building": ("IWG", "IW1", "IW2")
}

class Timetable_Class():
	def __init__(self, code, init_hour, end_hour, type, location, weeks, group=None):
		self.code = code
		self.name = self.get_module_name()
		self.hours = [self.parse_hour(init_hour), self.parse_hour(end_hour)]
		
		if type == "LEC":
			self.type = "Lecture"
		elif type == "TUT":
			self.type = "Tutorial"
		elif type == "LAB":
			self.type = "Laboratory"
		else:
			self.type = "Not Specified"

		self.location = self.parse_location(location)
		self.weeks = self.parse_weeks(weeks)	
		self.group = group

	def __str__(self):
		
		if self.group:
			return "Module {}, {}, from {:02d}:00 to {:02d}:00, {}, group {}, in {}, during {}-{},{}-{}".format(
					self.code,
					self.name,
					self.hours[0],
					self.hours[1],
					self.type, 
					self.group,
					self.location,
					self.weeks[0][0], self.weeks[0][1], self.weeks[1][0], self.weeks[1][1])
		else:
			return "Module {}, {}, from {:02d}:00 to {:02d}:00, {}, in {}, during {}-{},{}-{}".format(
					self.code,
					self.name,
					self.hours[0],
					self.hours[1],
					self.type, 
					self.location,
					self.weeks[0][0], self.weeks[0][1], self.weeks[1][0], self.weeks[1][1])
		
	def get_module_name(self):
		data = {"T1": str(self.code)}
		res = requests.post("http://www.timetable.ul.ie/tt_moduledetails_res.asp", data=data)
		
		module_soup = bs(res.text, "html.parser")
		mod_name_html = module_soup.find_all("tr")[2].find_all("td")[1]

		mod_name = mod_name_html.find("font").text
		mod_name = mod_name.split("\r\n")[0]

		return mod_name

	def parse_weeks(self, weeks):
		regex_1 = "Wks:(\d+)-(\d+)"
		regex_2 = "Wks:(\d+)-(\d+),(\d+)-(\d+)"

		parsed_weeks = None

		if len(re.compile(regex_1).split(weeks)) > 1:
			raw_weeks = re.compile(regex_1).split(weeks)
			parsed_weeks = [ [raw_weeks[1], raw_weeks[2]], ["", ""] ]

		elif len(re.compile(regex_2).split(weeks)) > 1:
			raw_weeks = re.compile(regex_2).split(weeks)
			parsed_weeks = [ [raw_weeks[1], raw_weeks[2]], [raw_weeks[3], raw_weeks[4]] ]

		return parsed_weeks

	def parse_location(self, location):
		splitted = re.compile("([A-Z]+)(\d+)").split(location)[1:-1]

		building = ""

		if splitted[0][-1:] in ("G", "M", "B"):
			if splitted[0] == "B":
				building = "Main Building"
			else:
				for key in building_dict:
					if splitted[0] in building_dict[key]:
						building = key
		else:
			b_tag = splitted[0] + splitted[1][0]
			for key in building_dict:
					if b_tag in building_dict[key]:
						building = key

		return building + " ({})".format(location)

	def parse_hour(self, hour):
		splitted = re.compile("(\d{2}):\d+").split(hour)
		return int(splitted[1])


def get_week_timetable(student_id):
	data = {"T1": student_id}
	html_body = requests.post("http://www.timetable.ul.ie/tt2.asp", data=data)

	soup = bs(html_body.text, "html.parser")

	# tr of all week
	timetable_html = soup.find_all("tr")[1]
	# each position, one day. List inside, each position, one class.
	week_timetable_html = [day.find_all("b") for day in tt_html.find_all("td")]
	week_timetable = []

	for day_timetable_html in week_timetable_html:
		day_timetable = []
		for subject in day_timetable_html:
			raw_vals = [x.split() for x in subject.text.split("\n")]
			group = raw_vals[6]

			if len(group) == 0:
				t = Timetable_Class(code=raw_vals[4][0], init_hour=raw_vals[0][0], end_hour=raw_vals[2][0], type=raw_vals[5][1], 
				location=raw_vals[8][0], weeks=raw_vals[11][0])
			else:
				t = Timetable_Class(code=raw_vals[4][0], init_hour=raw_vals[0][0], end_hour=raw_vals[2][0], type=raw_vals[5][1], 
				location=raw_vals[8][0], weeks=raw_vals[11][0], group=group[0])
			#print(t)
			day_timetable.append(t)
			
		week_timetable.append(day_timetable)
		#print("----------------------")

	return week_timetable




