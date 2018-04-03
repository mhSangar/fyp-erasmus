from utils.face_recognition_utils import train_classifier

model_path = "~/model_dir/20170512-110547/20170512-110547.pb"
classifier_path = "utils/face_recognition_utils/svc_classifier.pkl"

def recognise_face(face_img_path):
	student_name, percent = train_classifier.get_prediction(face_img_path, model_path, classifier_path)
	
	return student_name, percent