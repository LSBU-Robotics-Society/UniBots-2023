import cv2
import numpy as np
import apriltag

last_april_tags = []


def robot_to_cv_image(robot_image):
    npimage = np.frombuffer(bytearray(robot_image), dtype="uint8")
    cv_image_orig = cv2.imdecode(npimage, cv2.IMREAD_COLOR)
    cv_image = cv2.flip(cv_image_orig, 0)  # Flip vertical
    return cv_image


def cv_image_resize(cv_image, scale_percent):
    width = int(cv_image.shape[1] * scale_percent / 100)
    height = int(cv_image.shape[0] * scale_percent / 100)
    dim = (width, height)
    # resize image
    cv_image_scaled = cv2.resize(cv_image, dim, interpolation=cv2.INTER_AREA)
    return cv_image_scaled


def image_process(cv_image):
    image_out = cv_image.copy()

    #find_circles(cv_image, image_out)
    find_apriltags(cv_image, image_out)
    image_out = cv2.flip(image_out, 0)  # Flip vertical

    display(image_out)


def tag_visible(index):
    for r in last_april_tags:
        if r == index:
            return True
    
    return False


def tag_centre(index):
    for r in last_april_tags:
        if r == index:
            return r.center

    return []


def display(cv_image):
    cv2.imshow("OpenCV", cv_image)
    cv2.moveWindow("OpenCV", 50, 500)
    cv2.waitKey(3)


def find_circles(cv_image, output):
    gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.5, 50,
                               param1=80,
                               param2=50,
                               minRadius=2,
                               maxRadius=50)

    if circles is not None:
        # convert the (x, y) coordinates and radius of the circles to integers
        circles = np.round(circles[0, :]).astype("int")
        # loop over the (x, y) coordinates and radius of the circles
        for (x, y, r) in circles:
            # draw the circle in the output image, then draw a rectangle
            # corresponding to the center of the circle
            cv2.circle(output, (x, y), r, (255, 0, 0), 4)
            cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)


def find_apriltags(cv_image, output):
    # based on https://pyimagesearch.com/2020/11/02/apriltag-with-python/
    gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
    print("[INFO] detecting AprilTags...")
    options = apriltag.DetectorOptions(families="tag36h11")
    detector = apriltag.Detector(options)
    results = detector.detect(gray)
    print("[INFO] {} total AprilTags detected".format(len(results)))

    last_april_tags.clear()
    # loop over the AprilTag detection results
    for r in results:
        # extract the bounding box (x, y)-coordinates for the AprilTag
        # and convert each of the (x, y)-coordinate pairs to integers
        (ptA, ptB, ptC, ptD) = r.corners
        ptB = (int(ptB[0]), int(ptB[1]))
        ptC = (int(ptC[0]), int(ptC[1]))
        ptD = (int(ptD[0]), int(ptD[1]))
        ptA = (int(ptA[0]), int(ptA[1]))
        # draw the bounding box of the AprilTag detection
        cv2.line(output, ptA, ptB, (0, 255, 0), 2)
        cv2.line(output, ptB, ptC, (0, 255, 0), 2)
        cv2.line(output, ptC, ptD, (0, 255, 0), 2)
        cv2.line(output, ptD, ptA, (0, 255, 0), 2)
        # draw the center (x, y)-coordinates of the AprilTag
        (cX, cY) = (int(r.center[0]), int(r.center[1]))
        cv2.circle(output, (cX, cY), 5, (0, 0, 255), -1)
        # draw the tag family on the image
        # tagFamily = r.tag_family.decode("utf-8")
        tag_id = str(r.tag_id)
        cv2.putText(output, tag_id, (ptA[0], ptA[1] - 15),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        # print("[INFO] tag family: {}".format(tagFamily))

        last_april_tags.append(r.tag_id)

    return results
