# Intelligent Assistant with Face Recognition

## Final Year Project (FYP) - 2017/18 Course 

Author: Mario Sánchez García.
- Erasmus Student in the University of Limerick (Ireland), Science and Engineering Department of CSIS.
- Student in the University Carlos III of Madrid (Spain), Engineering School, Polytechnic Campus of Leganes.

### Abstract
This Final Year Project describes in detail the development of an _Intelligent Assistant_, whose objective will be to identify students of the University of Limerick using face recognition in order to provide them a personalised support. This support consists of showing what their next class in the day will be, hence the need to know the identity of the student, and then where will it be, showing a map with a path connecting the current position of the student to the location of the next class. The interaction with the _Intelligent Assistant_ will be through a graphical interface run by a small, low-cost and basic computer called Raspberry Pi. Due to the low computation power of this device, the application executed in the Raspberry Pi will communicate with a server located in another machine, which will actually perform the diverse tasks of the _Intelligent Assistant_.

The chosen approach to accomplish the face recognition are Convolutional Neural Networks, which have been widely used for image and video recognition in the recent years. Currently, one of the best face recognition implementations is FaceNet, with an accuracy close to 99.65\% in the latest tests. In their Github website they have provided several pre-trained models since the presentation of the paper, among which the Inception Resnet v1 model (20170512-110547) was chosen to be used in this project. Finally, the Tensorflow library for Python 3 was responsible to load and train this model with a new dataset to carry out the task of face recognition.
