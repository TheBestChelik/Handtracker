# Table of Contents
- [Table of Contents](#table-of-contents)
- [HandTracker](#handtracker)
  - [MouseControll.py](#mousecontrollpy)
  - [VolumeControll.py](#volumecontrollpy)
  - [CalibrateHand.py](#calibratehandpy)
  - [Additional functions](#additional-functions)
  - [Installation](#installation)
  - [Running MouseControll.py](#running-mousecontrollpy)
  - [Running VolumeControll.py](#running-volumecontrollpy)

# HandTracker
HandTracker contains few programs that let user control the computer via hand tracking. The project is based on [MediaPipe Hands](https://google.github.io/mediapipe/solutions/hands) for hand tracking and [cv2](https://pypi.org/project/opencv-python/) for capturing the video from the camera. At the moment there are two main and one calibration program.
## MouseControll.py
![](https://github.com/TheBestChelik/Handtracker/blob/main/img/MouseControl2.gif?raw=true)
The program monitors the forefinger movements and interprets it to the movement of the mouse on the screen. To press the left button of the mouse you should put down your middle finger, and to release it - return the finger to initial position.
## VolumeControll.py
![](https://github.com/TheBestChelik/Handtracker/blob/main/img/Volume2.gif?raw=true)

The following program adjusts the volume of the computer based on the distance between the middle and index fingers. Before the usage it is required to run the calibration program (`calibrateHand.py`) for the correct work of the program.
## CalibrateHand.py
![Calibrate](https://github.com/TheBestChelik/Handtracker/blob/main/img/calibrate2.gif?raw=true)

Calibration program was made for the correct work  of `VolumeControll.py`. For good calibration, the user should be in ordinary distance from the camera. During the calibration process you would be asked to connect your index finger with forefinger and to extend them. Follow the instructions that will appear on the screen.
## Additional functions
Likewise, there is `HandTrackerModule.py` that contains `class HandDetector()`. In this class you may find the `FindPos` function that returns the IDs of [hand-landmarks](https://google.github.io/mediapipe/solutions/hands#hand-landmark-model) and their coordinates on the image. 

In addition, there is a useful `FingersUp` function that specifies the state of the fingers on the hand (finger is up or down). 

`FindHands` function finds hands on images and highlights their [hand-landmarks](https://google.github.io/mediapipe/solutions/hands#hand-landmark-model)
![](https://github.com/TheBestChelik/Handtracker/blob/main/img/HandTracker2.gif?raw=true)


## Installation
Run
```bat 
  git repo clone TheBestChelik/Handtracker
```
Then install the requirements
```bat
  pip install -r requirements.txt 
```
## Running MouseControll.py
```bat
  python MouseControll.py
```
## Running VolumeControll.py
At first usage you have to calibrate settings file (`config`)
```bat
  python calibrateHand.py
```
Then you can run the VolumeControll.py
```bat
  python VolumeControll.py
```
