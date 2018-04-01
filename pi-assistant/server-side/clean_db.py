from app import app, db
from app.models import Student, Image, Face

print("Students:")
print(Student.query.all())

print("Faces:")
print(Face.query.all())

print("Images:")
print(Image.query.all())

for s in Student.query.all():
	db.session.delete(s)

for f in Face.query.all():
        db.session.delete(f)

for i in Image.query.all():
	db.session.delete(i)

db.session.commit()

print("\n\t>>>DATABASE CLEANED\n")
