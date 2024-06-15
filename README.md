# Run
Notes: 
- You must have this [camera](https://www.amazon.com/gp/product/B07R8LQKV4/ref=ppx_od_dt_b_asin_title_s00?ie=UTF8&psc=1). If you don't you will need to edit the software yourself. Please install any necessary packages.
- If you have multiple cameras please ensure the correct camera is being used by the program. If you think the wrong one is being selected go to the line with ```cam = cv2.VideoCapture(0)``` in ```script.py``` and increment the number until the right camera is selected.
```
git clone https://github.com/JoshuaChick/Yolov8StereoDepth
cd Yolov8StereoDepth
python script.py
```
Will give you a live video with labels and depths.

![alt text](https://github.com/JoshuaChick/Yolov8StereoDepth/blob/main/ReadMeImages/yoloWithDepths.png?raw=true)

# The Goal
Get this [camera](https://www.amazon.com/gp/product/B07R8LQKV4/ref=ppx_od_dt_b_asin_title_s00?ie=UTF8&psc=1) to do metric, stereo depth, on YOLOv8 output.

![alt text](https://github.com/JoshuaChick/Yolov8StereoDepth/blob/main/ReadMeImages/stereocam.jpg?raw=true)

# The Plan
The images from both cameras will be gathered.

![alt text](https://github.com/JoshuaChick/Yolov8StereoDepth/blob/main/ReadMeImages/camerasDiagram.png?raw=true)

Get the right image, as the base image. Run it through yolo.

![alt text](https://github.com/JoshuaChick/Yolov8StereoDepth/blob/main/ReadMeImages/rightCameraTakingPictureDiagram.png?raw=true)

![alt text](https://github.com/JoshuaChick/Yolov8StereoDepth/blob/main/ReadMeImages/objectInRightCamera.png?raw=true)

Run the left image through yolo, so now u have both left and right. 

![alt text](https://github.com/JoshuaChick/Yolov8StereoDepth/blob/main/ReadMeImages/objectInLeftAndRightCamera.png?raw=true)

Now you can work out angles from base of cameras to centres of those objects. And using the distance between the cameras you can trianglulate

![alt text](https://github.com/JoshuaChick/Yolov8StereoDepth/blob/main/ReadMeImages/stereoDepthMaths.png?raw=true)

## Technicalities
- To account for multiple of same object, pairs of the same object will be decided based on similarity of y-coord of top left corner of bounding box. (Going left to right will not work, you can look into this if you want (imagine something close and something far, etc...)).
- Depths of objects will be measured from right camera.

