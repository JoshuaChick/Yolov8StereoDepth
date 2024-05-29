# The Goal
Get this [camera](https://www.amazon.com/gp/product/B07R8LQKV4/ref=ppx_od_dt_b_asin_title_s00?ie=UTF8&psc=1) to do metric, stereo depth, on YOLOv8 output.
![alt text](https://github.com/JoshuaChick/Yolov8StereoDepth/blob/main/ReadMeImages/stereocam.jpg?raw=true)

# The Plan
The image from both cameras will be gathered.
![alt text](https://github.com/JoshuaChick/Yolov8StereoDepth/blob/main/ReadMeImages/camerasDiagram.png?raw=true)
Get the right image, as the base image. Run it through yolo.
![alt text](https://github.com/JoshuaChick/Yolov8StereoDepth/blob/main/ReadMeImages/rightCameraTakingPictureDiagram.png?raw=true)
![alt text](https://github.com/JoshuaChick/Yolov8StereoDepth/blob/main/ReadMeImages/objectInRightCamera.png?raw=true)
Run the left image through yolo, so now u have both left and right. 
![alt text](https://github.com/JoshuaChick/Yolov8StereoDepth/blob/main/ReadMeImages/rightCameraTakingPictureDiagram.png?raw=true)
Now you can work out angles from base of cameras to centre's of those objects. And using the distance between the cameras you can trianglulate
![alt text](https://github.com/JoshuaChick/Yolov8StereoDepth/blob/main/ReadMeImages/stereoDepthMaths.png?raw=true)

