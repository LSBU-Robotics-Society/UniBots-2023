import time

import robot_state
from robot_actions import *
import robot_interface as rb
import time

print("LED")
rb.flash_LED()
time.sleep(2)
rb.flash_LED()
time.sleep(2)

print("Camera")
image = rb.get_image()
vision.image_process(image)

print("Collision")
while not rb.get_command() == "":
    pass

for i in range(5):
    rb.check_collision()
    time.sleep(0.5)

    while not rb.get_command() == "":
        pass

    print("left  : " + str(robot_state.collision_left))
    print("Right : " + str(robot_state.collision_right))
    print("Back  : " + str(robot_state.collision_back))

print("Gate")
rb.gate_open()
time.sleep(2)
rb.gate_shut()
time.sleep(2)

print("Turning")
rb.turn_left()
time.sleep(2)
rb.turn_right()
time.sleep(2)
rb.turn_stop()
rb.move_stop()

print("Moving")
rb.move_forward()
time.sleep(1)
rb.move_stop()
time.sleep(1)
rb.move_backward()
time.sleep(1)
rb.move_stop()