import time
from robot_actions import *

t0 = time.perf_counter()

while True:
    image = rb.get_image()
    vision.image_process(image)
    print(time.perf_counter()-t0)
    time.sleep(100/1000)

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