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
	{"id": "17150868", "name": "Mario Sánchez García"},
	{"id": "17226163", "name": "Mark McNabola"},
#	{"id": " ", "name": " "},
#	{"id": " ", "name": " "},
#	{"id": " ", "name": " "},
#	{"id": " ", "name": " "},
#	{"id": " ", "name": " "},
#	{"id": " ", "name": " "},
	{"id": "00000000", "name": "<unknown>"}
]

for s in students:
	student = Student(id=s["id"], name=s["name"])
	print("\t" + student.__str__())
	db.session.add(student)

db.session.commit()
