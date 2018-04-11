from app import db

class Student(db.Model):
	id = db.Column(db.String(8), primary_key=True)
	name = db.Column(db.String(128), index=True)
	
	def __repr__(self):
		return "<Student: {}, ID: {}>".format(self.name, self.id)
