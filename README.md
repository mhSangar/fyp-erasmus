# Intelligent Assistant with Face Recognition

## Final Year Project (FYP) - 2017/18 Course 

	Mario Sánchez García, Erasmus Student, Dept. of CSIS, **University of Limerick** (Ireland) 

### Abstract
The aim of this project is to design and implement an Intelligent Assistant that recognises the face of a student, in order to provide personalised support. This support will consist of showing the student's timetable and the route to the lecture hall for their next class. The target of this project are students who are new to the University of Limerick, as they are the group that may need this service the most. Convolutional Neural Networks based on Google's Tensorflow library is used for face recognition. The application has two aspects. The first is a Raspberry Pi used to capture a face image and transmit it to a Flask server. The second, a server that runs the classifier used to recognise the student, retrieve their personal timetable, and display the route to the next lecture hall.

<!--
The aim of this project is to design and implement an intelligent assistant, whose objective will be to recognise and identify the face of a person in order to give personalised support. There are multiple approaches on how to develop this face recognisement, but in this case we have chosen Convolutional Neural Networks by using the open source library TensorFlow (originally developed by Google). However, the calculations done by this library need the computer used to have a certain power, which supposes it also will have a considerable size.

To achieve a lightweight structure (and increase the programming load of the project) the system is divided in two independent applications. First, a Raspberry Pi 3 is going to be used to get the data from the camera and act as the user interface. This Raspberry will communicate as a client with a Flask Server allocated in another machine with higher specs, which will use the data captured by the camera and the TensorFlow library to procced with the facial recognition (as well as help the user in the support he/she requires). 
-->
