from app import app, db
from app.models import Student, Image
import os

basedir = os.path.abspath(os.path.dirname(__file__))

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Student': Student, 'Image': Image, \
    'basedir': basedir, 'os': os}