# Finger Counter Using Hand Tracking

This project counts how many fingers are raised in real time using computer vision and hand landmark detection. The application reads a live camera stream, detects the hand, determines the number of raised fingers, and displays an image that matches the detected count.


## Project Overview
The program uses a hand detector to locate landmarks on the hand. It then compares landmark positions to decide whether each finger is raised. The detected number is used to overlay an image from a Pictures folder onto the video frame.


## Key Features
* Real time finger counting from a live camera stream
* Uses hand landmarks to detect raised fingers
* Overlays an image that matches the finger count
* Multi threaded design for capture, processing, and display
* Works with an IP camera stream such as DroidCam

<img width="450" height="500" alt="image" src="https://github.com/user-attachments/assets/080a6f86-645d-4ff6-b28a-e0a704d3f331" />

## Technologies and Libraries
* Python
* OpenCV
* MediaPipe through the HandDetector module
* Threading and Queue

## Project Structure
```
finger_counter/
finger_counter.py
HandDetector.py
Pictures/
README.md
```

## Camera Configuration
The project uses an IP camera stream. Update the URL inside the code if needed.

```python
URL = "http://192.168.1.2:4747/video"
```

Ensure your phone camera and your PC are connected to the same local network.


## Pictures Folder Setup
Create a folder named Pictures in the project directory. Place images inside it that represent each finger count.

Recommended mapping
* Image 1 shows 1 finger
* Image 2 shows 2 fingers
* Image 3 shows 3 fingers
* Image 4 shows 4 fingers
* Image 5 shows 5 fingers


## How Finger Counting Works
The program checks fingertip landmarks and compares them with lower joint landmarks to determine whether a finger is raised.
<img width="450" height="500" alt="5 Hand" src="https://github.com/user-attachments/assets/152fae15-0c7c-4a2f-a252-0baa59c5bb4f" />


## Running the Application
```bash
python finger_counter.py
```

Press Q to exit the application.


## Dependencies
```
opencv-python
mediapipe
```

Additional dependencies may be required by the HandDetector module.

## License
This project is licensed under the MIT License.

## Author
Ali Hassoneh

