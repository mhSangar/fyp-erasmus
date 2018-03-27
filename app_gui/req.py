import requests
import json
from bs4 import BeautifulSoup as bs

data = {"T1": "CS4618"}
res = requests.post("http://www.timetable.ul.ie/tt_moduledetails_res.asp", data=data)

module_soup = bs(res.text, "html.parser")
mod_name_html = module_soup.find_all("tr")[2].find_all("td")[1]

print(module_soup.find_all("tr")[2].find_all("td")[1].find("font").text.split("\r\n"))
