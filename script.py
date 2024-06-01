import torch
import cv2
import time
from ultralytics import YOLO


model = YOLO("yolov8n.pt")
# yolo outputs classes as numbers, this translates that to strings
num_to_name = {
    0: 'person',
    1: 'bicycle',
    2: 'car',
    3: 'motorcycle',
    4: 'airplane',
    5: 'bus',
    6: 'train',
    7: 'truck',
    8: 'boat',
    9: 'traffic light',
    10: 'fire hydrant',
    11: 'stop sign',
    12: 'parking meter',
    13: 'bench',
    14: 'bird',
    15: 'cat',
    16: 'dog',
    17: 'horse',
    18: 'sheep',
    19: 'cow',
    20: 'elephant',
    21: 'bear',
    22: 'zebra',
    23: 'giraffe',
    24: 'backpack',
    25: 'umbrella',
    26: 'handbag',
    27: 'tie',
    28: 'suitcase',
    29: 'frisbee',
    30: 'skis',
    31: 'snowboard',
    32: 'sports ball',
    33: 'kite',
    34: 'baseball bat',
    35: 'baseball glove',
    36: 'skateboard',
    37: 'surfboard',
    38: 'tennis racket',
    39: 'bottle',
    40: 'wine glass',
    41: 'cup',
    42: 'fork',
    43: 'knife',
    44: 'spoon',
    45: 'bowl',
    46: 'banana',
    47: 'apple',
    48: 'sandwich',
    49: 'orange',
    50: 'broccoli',
    51: 'carrot',
    52: 'hot dog',
    53: 'pizza',
    54: 'donut',
    55: 'cake',
    56: 'chair',
    57: 'couch',
    58: 'potted plant',
    59: 'bed',
    60: 'dining table',
    61: 'toilet',
    62: 'tv',
    63: 'laptop',
    64: 'mouse',
    65: 'remote',
    66: 'keyboard',
    67: 'cell phone',
    68: 'microwave',
    69: 'oven',
    70: 'toaster',
    71: 'sink',
    72: 'refrigerator',
    73: 'book',
    74: 'clock',
    75: 'vase',
    76: 'scissors',
    77: 'teddy bear',
    78: 'hair drier',
    79: 'toothbrush'
}
name_to_num = {}
for key in num_to_name:
    name_to_num[num_to_name[key]] = key


def split_camera_feed(img):
    """
    As the camera feed combines both cameras images into one, this function will split it and return the individual images.
    """
    # shape assumes img is in h, w, c (default format of cv2 video capture frame)
    shape = img.shape
    width = shape[1]
    half_width = int(width / 2)
    return img[:, :half_width, :], img[:, half_width:, :]


def determine_depths(left_img, left_yolo_results, right_img, right_yolo_results):
    """
    Determines depths of every object in right_img. Returns a list of depths, the order of which corresponds to the
    order of the right_yolo_results (e.g., if first depth is 1m and first object in results is person -> person is
    1m away).
    """
    pass


def determine_depth(left_img, left_center_coords, right_img, right_center_coords):
    """
    determine_depths(), once it has paired up bounding boxes between left and right, will use this function to calculate
    the depth for each individual object. I mainly included this function so others can copy-paste it if they want to do
    depth calculations in separate projects, as its parameters aren't for a YOLO specific object.
    """
    pass


if __name__ == '__main__':
    cam = cv2.VideoCapture(1)

    ret, frame = cam.read()

    l, r = split_camera_feed(frame)

    result = model(r)[0].boxes
    print(result)

    cam.release()
    cv2.destroyAllWindows()



