import cv2
import settings

if not settings.USE_SIM_CAMERA:
    cam = cv2.VideoCapture(1)
    #cam.set(cv2.CAP_PROP_FRAME_WIDTH,256)
    #cam.set(cv2.CAP_PROP_FRAME_HEIGHT,256)

def get_image():
    status, image = cam.read()
    #image = cv2.flip(image, 0)  # Flip vertical
    return image
