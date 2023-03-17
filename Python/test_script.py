import time
from robot_actions import *
import robot_interface as rb
import time

print("LED")
rb.flash_LED()
time.sleep(2)
rb.flash_LED()
time.sleep(2)

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
