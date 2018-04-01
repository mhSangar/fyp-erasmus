import os
import logging

basedir = os.path.abspath(os.path.dirname(__file__))
# disables TensorFlow warnings about AVX/FMA support
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
# sets the log pattern
logging.basicConfig(level=logging.INFO, format="[%(levelname)s] : %(message)s")

class Config(object):
	SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "sqlite:///" + os.path.join(basedir, "app.db")
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	PI_CAPTURES_FOLDER_PATH = os.path.join(basedir, "app/pi_captures/")
	 
