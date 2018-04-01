#!flask/bin/python
#from flask import Flask, jsonify, abort, make_response, request
#from flask_sqlalchemy import SQLAlchemy
#import os
#
#basedir = os.path.abspath(os.path.dirname(__file__))
#
#app = Flask(__name__)
#app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "server-db.db")
#app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#db = SQLAlchemy(app)
#
#@app.errorhandler(404)
#def not_found(error):
#    return make_response(jsonify({'error': 'Resource not found'}), 404)
#
#@app.route("/")
#def index():
#	return "Intelligent Assistant for FYP by Mario Sanchez Garcia"
#
#@app.route("/face_recog/imgs", methods=["GET"])
#def get_imgs():
#	return jsonify({"img":0})
#
#if __name__ == "__main__":
#	app.run(debug=True)

from app import app, db
from app.models import Student, Image
import os

basedir = os.path.abspath(os.path.dirname(__file__))


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Student': Student, 'Image': Image, \
    'basedir': basedir, 'os': os}