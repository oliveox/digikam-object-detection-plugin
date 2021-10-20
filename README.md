# Digikam Object Detection "Plugin"
Gives the ability to search media files inside a DigiKam collection by the objects they contain

# How does it work?
The interface between the DigiKam UI and this Python project is the DigiKam SQLite database, in which this "plugin" inserts the objects detected in the DigiKam collection files.

# Install
## Prerequisites
- Python >= 3.8
- DigiKam >= 7.1.0

## Steps
1. clone this project
2. `cd` inside the project
3. optional: create a virtual environment and activate it
4. `pip install -r requirements.txt`
5. `pip install -r https://raw.githubusercontent.com/ultralytics/yolov5/master/requirements.txt`
6. `cd src`
7. `cp .env-example .env`
8. fill up the .env file with your specific paths
7. `python main.py`

# Support

## Operating Systems
- Linux (tested on Ubuntu 20.04)
- Windows (tested on Windows 10)

## Media files
- images

## Machine Learning Processing Hardware
- CPU

# Contribute
Drop an issue if you have any questions, suggestions or observations. Other not yet implemented cool features I've been thinking about can be found in the TODO file or in code marked with //TODO.

# Credits
The object detection core is [YOLOv5](https://github.com/ultralytics/yolov5)