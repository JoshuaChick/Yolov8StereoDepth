import torch
import cv2


def split_camera_feed(img):
    """
    As the camera feed combines both cameras images into one, this function will split it and return the individual images.
    """
    pass


def determine_depths(left_img, left_yolo_results, right_img, right_yolo_results):
    """
    Determines depths of every object in right_img. Returns a list of depths, the order of which corresponds to the
    order of the right_yolo_results (e.g., if first depth is 1m and first object in results is person -> person is
    1m away).
    """
    pass


if __name__ == '__main__':
    pass



