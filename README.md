# The Goal
Get this [camera](https://www.amazon.com/gp/product/B07R8LQKV4/ref=ppx_od_dt_b_asin_title_s00?ie=UTF8&psc=1) to do metric, stereo depth, on YOLOv8 output.
![alt text](https://github.com/JoshuaChick/Yolov8StereoDepth/blob/main/ReadMeImages/stereocam.jpg?raw=true)

# The Plan
In order not to make the one camera zones too big (these are problematic as you cannot do stereo depth in them), the right side of the right camera feed will be cropped, and the same with the left.
![alt text](https://github.com/JoshuaChick/Yolov8StereoDepth/blob/main/ReadMeImages/ThePlanDiagram.png?raw=true)
Now as the one camera zone is fairly small, it will be assumed any time an object appears in the right camera we can match it to the left camera and triangulate depth on the x and y plain, which will then let us calculate depth (D or z).
![alt text](https://github.com/JoshuaChick/Yolov8StereoDepth/blob/main/ReadMeImages/stereoDepthMaths.png?raw=true)

