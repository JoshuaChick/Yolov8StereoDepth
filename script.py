import math
import torch
import cv2
import time
from ultralytics import YOLO


device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
model = YOLO('yolov8x.pt').to(device)

# yolo outputs classes as numbers, this translates that to strings
num_to_name = {0: 'person', 1: 'bicycle', 2: 'car', 3: 'motorcycle', 4: 'airplane', 5: 'bus', 6: 'train', 7: 'truck', 8: 'boat', 9: 'traffic light', 10: 'fire hydrant', 11: 'stop sign', 12: 'parking meter', 13: 'bench', 14: 'bird', 15: 'cat', 16: 'dog', 17: 'horse', 18: 'sheep', 19: 'cow', 20: 'elephant', 21: 'bear', 22: 'zebra', 23: 'giraffe', 24: 'backpack', 25: 'umbrella', 26: 'handbag', 27: 'tie', 28: 'suitcase', 29: 'frisbee', 30: 'skis', 31: 'snowboard', 32: 'sports ball', 33: 'kite', 34: 'baseball bat', 35: 'baseball glove', 36: 'skateboard', 37: 'surfboard', 38: 'tennis racket', 39: 'bottle', 40: 'wine glass', 41: 'cup', 42: 'fork', 43: 'knife', 44: 'spoon', 45: 'bowl', 46: 'banana', 47: 'apple', 48: 'sandwich', 49: 'orange', 50: 'broccoli', 51: 'carrot', 52: 'hot dog', 53: 'pizza', 54: 'donut', 55: 'cake', 56: 'chair', 57: 'couch', 58: 'potted plant', 59: 'bed', 60: 'dining table', 61: 'toilet', 62: 'tv', 63: 'laptop', 64: 'mouse', 65: 'remote', 66: 'keyboard', 67: 'cell phone', 68: 'microwave', 69: 'oven', 70: 'toaster', 71: 'sink', 72: 'refrigerator', 73: 'book', 74: 'clock', 75: 'vase', 76: 'scissors', 77: 'teddy bear', 78: 'hair drier', 79: 'toothbrush'}
name_to_num = {}
for key in num_to_name:
    name_to_num[num_to_name[key]] = key

# camera fov in degrees, for horizontal and vertical, max should be 180
CAMERA_FOV_X = 120
CAMERA_FOV_Y = 60
# distance between cameras, cms
DISTANCE_BETWEEN_CAMERAS = 6


def split_camera_feed(img):
    """
    As the camera feed combines both cameras images into one, this function will split it and return the individual images.
    """
    # shape assumes img is in h, w, c (default format of cv2 video capture frame)
    shape = img.shape
    width = shape[1]
    half_width = int(width / 2)
    return img[:, :half_width, :], img[:, half_width:, :]


def if_zero_return_epsilon(n):
    if n == 0:
        return 0.000001
    else:
        return n


def determine_depths(left_img, left_yolo_results, right_img, right_yolo_results):
    """
    Determines depths of every object in right_img. Returns a list of depths, the order of which corresponds to the
    order of the right_yolo_results (e.g., if first depth is 1m and first object in results is person -> person is
    1m away).
    """
    left_boxes = left_yolo_results[0].boxes
    right_boxes = right_yolo_results[0].boxes

    # list of depths for each object in right image. Will be returned at end
    list_right_object_depths = []

    # the algorithm for finding depths is:
    # 1. Start with first object right image (according to how YOLO outputted them)
    # 2. Pair that up to object in left image (based on the object with most similar y-value)
    # 3. Calculate depth with this pair
    # 4. Exclude both those images from being used in future iterations
    # 5. Repeat until no more objects in right image

    left_object_indexes_already_paired = []

    # 1. 4. and 5.
    for r_idx, r_class_num in enumerate(right_boxes.cls):
        r_xyxy = right_boxes.xyxy[r_idx]

        r_y_coord = r_xyxy[1]

        l_index_of_most_similar_y = -1
        most_recent_y_abs_diff = -1

        # 2.
        for l_idx, l_class_num in enumerate(left_boxes.cls):
            if l_class_num != r_class_num or l_idx in left_object_indexes_already_paired:
                continue
            else:
                l_xyxy = left_boxes.xyxy[l_idx]
                l_y_coord = l_xyxy[1]
                if most_recent_y_abs_diff == -1:
                    most_recent_y_abs_diff = abs(r_y_coord - l_y_coord)
                    l_index_of_most_similar_y = l_idx
                else:
                    # walrus operator diff gets assigned to ycoord - ycoord and returns itself for comparison
                    if (diff := abs(r_y_coord - l_y_coord)) < most_recent_y_abs_diff:
                        most_recent_y_abs_diff = diff
                        l_index_of_most_similar_y = l_idx

        # 3.
        # this means no match was found
        if l_index_of_most_similar_y == -1:
            list_right_object_depths.append('-')
        else:
            # right_centre_x
            r_c_x = int((r_xyxy[0] + r_xyxy[2]) / 2)
            r_c_y = int((r_xyxy[1] + r_xyxy[3]) / 2)
            l_c_x = int((l_xyxy[0] + l_xyxy[2]) / 2)
            l_c_y = int((l_xyxy[1] + l_xyxy[3]) / 2)

            list_right_object_depths.append(
                determine_depth(
                    left_img,
                    (l_c_x, l_c_y),
                    right_img,
                    (r_c_x, r_c_y)
                )
            )

            # 4.
            left_object_indexes_already_paired.append(l_index_of_most_similar_y)

    return list_right_object_depths


def determine_depth(left_img, obj_center_coords_left_cam, right_img, obj_center_coords_right_cam):
    """
    determine_depths(), once it has paired up bounding boxes between left and right, will use this function to calculate
    the depth for each individual object. I mainly included this function so others can copy-paste it if they want to do
    depth calculations in separate projects, as its parameters aren't for a YOLO specific object.
    """
    # this program assumes same camera used for both views, so doesn't matter if left or right used here:
    width_img = left_img.shape[1]
    height_img = left_img.shape[0]

    centre_x_of_cam = int(width_img / 2)
    centre_y_of_cam = int(height_img / 2)

    angle_to_start_of_fov_x = 90 - int(CAMERA_FOV_X / 2)
    angle_to_start_of_fov_y = 90 - int(CAMERA_FOV_Y / 2)

    obj_centre_x_r = obj_center_coords_right_cam[0]
    obj_centre_y_r = obj_center_coords_right_cam[1]
    obj_centre_x_l = obj_center_coords_left_cam[0]

    # angle between board and line of sight to obj from left and right camera
    angle_of_obj_btwn_board_los_l_cam = 180 - (int((obj_centre_x_l / width_img) * CAMERA_FOV_X) + angle_to_start_of_fov_x)
    angle_of_obj_btwn_board_los_r_cam = int((obj_centre_x_r / width_img) * CAMERA_FOV_X) + angle_to_start_of_fov_x

    angle_at_obj = 180 - angle_of_obj_btwn_board_los_l_cam - angle_of_obj_btwn_board_los_r_cam

    if 0 <= angle_at_obj < 1:
        return 'far away'
    elif angle_at_obj < 0:
        return '-'

    # this angle is the los from the flat horizontal line passing through the middle of the right image (doesn't matter if positive or negative)
    angle_of_obj_btwn_horizon_los_r_cam = 0
    if obj_centre_y_r == centre_y_of_cam:
        pass
    elif obj_centre_y_r > centre_y_of_cam:
        angle_of_obj_btwn_horizon_los_r_cam = int((obj_centre_y_r / height_img) * CAMERA_FOV_Y) + angle_to_start_of_fov_y - 90
    else:
        angle_of_obj_btwn_horizon_los_r_cam = 90 - (int((obj_centre_y_r / height_img) * CAMERA_FOV_Y) + angle_to_start_of_fov_y)



    ##### TRIG SECTION #####
    # x goes across camera, y goes up camera, z plane goes into camera. x z only means line to object w/o accounting for
    # drop or elevation (i.e., no y plane)
    # 1. object lies on vertical centre line of left camera
    if obj_centre_x_l == centre_x_of_cam:
        if obj_centre_x_r >= centre_x_of_cam:
            # this means that it was wrong object, you can do the geometry if you want
            return '-'
        x_z_only_line_from_right = DISTANCE_BETWEEN_CAMERAS / if_zero_return_epsilon(math.cos(math.radians(angle_of_obj_btwn_board_los_r_cam)))
        if obj_centre_y_r == centre_y_of_cam:
            return x_z_only_line_from_right
        else:
            # this works for both los being above and below horizon line
            return x_z_only_line_from_right / if_zero_return_epsilon(math.cos(math.radians(angle_of_obj_btwn_horizon_los_r_cam)))



    # 2. object lies on v. centre line of right camera
    elif obj_centre_x_r == centre_x_of_cam:
        if obj_centre_x_l <= centre_x_of_cam:
            # this means that it was wrong object, you can do the geometry if you want
            return '-'
        x_z_only_line_from_right = DISTANCE_BETWEEN_CAMERAS * math.tan(math.radians(angle_of_obj_btwn_board_los_l_cam))
        if obj_centre_y_r == centre_y_of_cam:
            return x_z_only_line_from_right
        else:
            return x_z_only_line_from_right / if_zero_return_epsilon(math.cos(math.radians(angle_of_obj_btwn_horizon_los_r_cam)))



    # 3. object lies between v. centres of left and right cameras
    elif obj_centre_x_r < centre_x_of_cam and obj_centre_x_l > centre_x_of_cam:
        line_from_r_between_board_and_r_los = DISTANCE_BETWEEN_CAMERAS * math.sin(math.radians(angle_of_obj_btwn_board_los_l_cam))
        x_z_only_line_from_right = line_from_r_between_board_and_r_los / if_zero_return_epsilon(math.sin(math.radians(angle_at_obj)))
        return x_z_only_line_from_right / if_zero_return_epsilon(math.cos(math.radians(angle_of_obj_btwn_horizon_los_r_cam)))



    # 4. object lies left of v. centre of left camera (and hence should be left of centre of right)
    elif obj_centre_x_l < centre_x_of_cam:
        if obj_centre_x_r > centre_x_of_cam:
            return '-'
        line_from_l_between_board_and_l_los = DISTANCE_BETWEEN_CAMERAS * math.sin(math.radians(angle_of_obj_btwn_board_los_r_cam))
        first_part_of_x_z_only_line_from_right = DISTANCE_BETWEEN_CAMERAS * math.cos(math.radians(angle_of_obj_btwn_board_los_r_cam))
        second_part_of_x_z_only_line_from_right = line_from_l_between_board_and_l_los / if_zero_return_epsilon(math.tan(math.radians(angle_at_obj)))
        x_z_only_line_from_right = first_part_of_x_z_only_line_from_right + second_part_of_x_z_only_line_from_right
        return x_z_only_line_from_right / if_zero_return_epsilon(math.cos(math.radians(angle_of_obj_btwn_horizon_los_r_cam)))



    # 5. object lies right of v. centre of right camera (and hence should be right of centre of left)
    elif obj_centre_x_r > centre_x_of_cam:
        if obj_centre_x_l < centre_x_of_cam:
            return '-'
        line_from_r_between_board_and_r_los = DISTANCE_BETWEEN_CAMERAS * math.sin(math.radians(angle_of_obj_btwn_board_los_l_cam))
        x_z_only_line_from_right = line_from_r_between_board_and_r_los / if_zero_return_epsilon(math.sin(math.radians(angle_at_obj)))
        return x_z_only_line_from_right / if_zero_return_epsilon(math.cos(math.radians(angle_of_obj_btwn_horizon_los_r_cam)))


if __name__ == '__main__':
    # lower three lines set a custom video resolution, if you want cv2's default, uncomment first and comment out
    # lower three
    # cam = cv2.VideoCapture(0)
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 2560)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 960)

    start = time.time()

    while time.time() - start <= 60:
        ret, frame = cam.read()

        l, r = split_camera_feed(frame)

        l_results = model(l, verbose=False)
        r_results = model(r, verbose=False)
        r_boxes = r_results[0].boxes

        r_depths = determine_depths(l, l_results, r, r_results)

        # displaying bounding boxes
        for i, c in enumerate(r_boxes.cls):
            depth_cms = r_depths[i]

            # if it couldn't get depth will not display bounding box
            if depth_cms == '-':
                continue

            xyxy = r_boxes.xyxy[i]

            x_1 = int(xyxy[0])
            y_1 = int(xyxy[1])
            x_2 = int(xyxy[2])
            y_2 = int(xyxy[3])

            cv2.rectangle(r, (x_1, y_1), (x_2, y_2), (0, 255, 0), 2)

            depth_text = ''

            if depth_cms == 'far away':
                depth_text = depth_cms
            elif depth_cms < 0:
                depth_text = '0 m'
            else:
                depth_meters = depth_cms / 100
                depth_text = f'{depth_meters:.2f} m'

            cv2.putText(r, f'{num_to_name[int(c)]} {depth_text}', (x_1, y_1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)

        cv2.imshow('', r)
        cv2.waitKey(1)

    cam.release()
    cv2.destroyAllWindows()



