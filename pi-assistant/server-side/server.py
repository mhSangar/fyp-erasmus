from app import app, db
from app.models import Student
import os

basedir = os.path.abspath(os.path.dirname(__file__))

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Student': Student, 'basedir': basedir, 'os': os}