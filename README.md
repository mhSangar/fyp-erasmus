# Intelligent Assistant with Face Recognition

## Final Year Project (FYP) - 2017/18 Course 

	_Mario Sánchez García_, Erasmus Student, Dept. of CSIS, **University of Limerick** (Ireland) 

### Abstract
The aim of this project is to design and implement an intelligent assistant, whose objective will be to recognise and identify the face of a person in order to give personalised support. There are multiple approaches on how to develop this face recognisement, but in this case we have chosen Convolutional Neural Networks by using the open source library TensorFlow (originally developed by Google). However, the calculations done by this library need the computer used to have a certain power, which supposes it also will have a considerable size.

To achieve a lightweight structure (and increase the programming load of the project) the system is divided in two independent applications. First, a Raspberry Pi 3 is going to be used to get the data from the camera and act as the user interface. This Raspberry will communicate as a client with a Flask Server allocated in another machine with higher specs, which will use the data captured by the camera and the TensorFlow library to procced with the facial recognition (as well as help the user in the support he/she requires). 