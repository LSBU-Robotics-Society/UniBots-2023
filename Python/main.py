import time
import threading
from robot_actions import *
import serial.tools.list_ports
import os



t0 = time.perf_counter()

def serial_thread():
    global t0
    while True:
        myports =[tuple(p) for p in list(serial.tools.list_ports.comports())]
        if len(myports) == 0:
            os.system("sudo shutdown now")
        else:
            if get_serial() == "Y":
                t0 = time.perf_counter()
                #start_command = 1
    
def robot_thread():
    global t0
    while True:
        image = rb.get_image()
        vision.image_process(image)
        print(time.perf_counter()-t0)
        time.sleep(1/1000)
        if time.perf_counter() > (t0+120):
            dead_stop()
        elif time.perf_counter() >= (t0+10):
            move_to_home()
        elif time.perf_counter() < (t0+2):
            rb.turn_stop()
            rb.move_forward()
        elif time.perf_counter() < (t0 + 3.5):
            rb.move_stop()
            rb.turn_left()
        elif time.perf_counter() < (t0 + 5):
            rb.turn_stop()
            rb.move_forward()
        elif time.perf_counter() < (t0 + 6.5):
            rb.move_stop()
            rb.turn_right()
        elif time.perf_counter() < (t0 + 8.5):
            rb.turn_stop()
            rb.move_forward()
        elif time.perf_counter() < (t0 + 10):
            rb.move_stop()
            rb.turn_stop()
        else:
            dead_stop()

serialThread = threading.Thread(target=serial_thread)
robotThread  = threading.Thread(target=robot_thread)
serialThread.start()
robotThread.start()