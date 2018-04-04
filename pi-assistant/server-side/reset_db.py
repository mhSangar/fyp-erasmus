from app import app, db
from app.models import Student
#from app.models import Image, Face

print("Students:")
for s in Student.query.all():
	print("\t" + s.__str__())

#print("Faces:")
#print(Face.query.all())

#print("Images:")
#print(Image.query.all())

for s in Student.query.all():
	db.session.delete(s)

#for f in Face.query.all():
#        db.session.delete(f)

#for i in Image.query.all():
#	db.session.delete(i)

db.session.commit()

print("\n  >>>>>>>>> DATABASE RESETED\n")

print("New students:")

students = [
	{"id": "17226163", "name": "Mario Sánchez García"},
	{"id": "17196906", "name": "Tang Jiaxuan"},
	{"id": "17198046", "name": "Harrison Ford"},
	{"id": "17198232", "name": "Nicole Kidman"},
	{"id": "17204178", "name": "Angelina Jolie"},
	{"id": "17206286", "name": "Igor Ivanov"},
	{"id": "17210577", "name": "Ann Veneman"},
	{"id": "17231728", "name": "Serena Williams"},
	{"id": "17235251", "name": "Keanu Reeves"},
	{"id": "00000000", "name": "<unknown>"}
]

for s in students:
	student = Student(id=s["id"], name=s["name"])
	print("\t" + student.__str__())
	db.session.add(student)

db.session.commit()
