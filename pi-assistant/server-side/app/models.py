from app import db

class Student(db.Model):
	id = db.Column(db.String(8), primary_key=True)
	name = db.Column(db.String(128), index=True)
	# list of images, link 1:n to another table
	images = db.relationship("Face", backref="student", lazy="dynamic")

	def __repr__(self):
		return "<Student: {}, ID: {}>".format(self.name, self.id)

class Face(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	img = db.Column(db.String)
	student_id = db.Column(db.String(8), db.ForeignKey("student.id"))

	def __repr__ (self):
		filename = self.img.split("/")[-1]
		return "<Image {}, Student: {}>".format(filename, self.student_id)

class Image(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	img = db.Column(db.String)

	def __repr__ (self):
		filename = self.img.split("/")[-1]
		return "<Image {}>".format(filename)