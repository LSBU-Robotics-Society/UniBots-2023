import cv2
import settings

if not settings.USE_SIM_CAMERA:
    cam = cv2.VideoCapture(0)


def get_image():
    status, image = cam.read()
    return image
