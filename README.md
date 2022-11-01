# Table of Contents
- [Table of Contents](#table-of-contents)
- [HandTracker](#handtracker)
  - [MouseControll.py](#mousecontrollpy)
  - [VolumeControll.py](#volumecontrollpy)
  - [CalibrateHand.py](#calibratehandpy)
  - [Additional functions](#additional-functions)
  - [Installation](#installation)

# HandTracker
HandTracker contains few programs that let user control the computer via hand tracking. The project is based on [MediaPipe Hands](https://google.github.io/mediapipe/solutions/hands) for hand tracking and [cv2](https://pypi.org/project/opencv-python/) for capturing the video from the camera. At the moment there are two main and one calibration program.
## MouseControll.py
![](https://github.com/TheBestChelik/Handtracker/blob/main/img/MouseControl.gif?raw=true)
Program monitors the forefinger movements and interprets it to the movement of the mouse on the screen. To press the left button of the mouse you should put down your middle finger, and to release it - return the finger to initial position.
## VolumeControll.py
![](https://github.com/TheBestChelik/Handtracker/blob/main/img/Volume.gif?raw=true)

The following program adjusts the volume of the computer based on the distance between the middle and index fingers. Before the usage it is required to run the calibration program (`calibrateHand.py`) for the correct work of the program.
## CalibrateHand.py
![Calibrate](https://github.com/TheBestChelik/Handtracker/blob/main/img/calibrate.gif?raw=true)

Calibration program was made for the correct work  of `VolumeControll.py`. For good calibration, the user should be in ordinary distance from the camera.
## Additional functions
Likewise, there is `HandTrackerModule.py` that contains `class HandDetector()`. In this class you may find the `FindPos` function that returns the IDs of [hand-landmarks](https://google.github.io/mediapipe/solutions/hands#hand-landmark-model) and their coordinates on the image. 

In addition, there is a useful `FingersUp` function that specifies the state of the fingers on the hand (finger is up or down). 

`FindHands` function finds hands on images and highlights their [hand-landmarks](https://google.github.io/mediapipe/solutions/hands#hand-landmark-model)
![](https://github.com/TheBestChelik/Handtracker/blob/main/img/HandTracker.gif?raw=true)

## Installation
