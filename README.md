# Run
Notes: 
- You should have this [camera](https://www.amazon.com/gp/product/B07R8LQKV4/ref=ppx_od_dt_b_asin_title_s00?ie=UTF8&psc=1). If you don't you may need to edit the software yourself.
- Please install any necessary packages.
- If you have multiple cameras please ensure the correct camera is being used by the program. If you think the wrong one is being selected go to the line with ```cam = cv2.VideoCapture(0)``` in ```script.py``` and increment the number until the correct camera is selected.
```
git clone https://github.com/JoshuaChick/Yolov8StereoDepth
cd Yolov8StereoDepth
python script.py
```
Will give you a live video with labels and depths.

https://github.com/user-attachments/assets/f494a8e4-23da-49a2-88b2-7d7e281ef7df

# Overview
Got this [camera](https://www.amazon.com/gp/product/B07R8LQKV4/ref=ppx_od_dt_b_asin_title_s00?ie=UTF8&psc=1) to do metric, stereo depth, on YOLOv8 output.

![alt text](https://github.com/JoshuaChick/Yolov8StereoDepth/blob/main/ReadMeImages/stereocam.jpg?raw=true)

# How It Works
The images from both cameras are gathered.

![alt text](https://github.com/JoshuaChick/Yolov8StereoDepth/blob/main/ReadMeImages/camerasDiagram.png?raw=true)

Right image run through yolo.

![alt text](https://github.com/JoshuaChick/Yolov8StereoDepth/blob/main/ReadMeImages/rightCameraTakingPictureDiagram.png?raw=true)

![alt text](https://github.com/JoshuaChick/Yolov8StereoDepth/blob/main/ReadMeImages/objectInRightCamera.png?raw=true)

Left image through yolo. Now left and right have been run through yolo. 

![alt text](https://github.com/JoshuaChick/Yolov8StereoDepth/blob/main/ReadMeImages/objectInLeftAndRightCamera.png?raw=true)

Work out angles from base of cameras to centres of those objects. And using the distance between the cameras you can trianglulate

![alt text](https://github.com/JoshuaChick/Yolov8StereoDepth/blob/main/ReadMeImages/stereoDepthMaths.png?raw=true)

## Technicalities
- To account for multiple of same object, pairs of the same object are decided based on similarity of y-coord of top left corner of bounding box. (Going left to right will not work, you can look into this if you want (imagine something close and something far, etc...)).
- Depths of objects are measured from right camera.

