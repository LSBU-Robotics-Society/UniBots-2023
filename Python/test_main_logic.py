import time
import threading

import robot_actions
import robot_state
from robot_actions import *
import serial.tools.list_ports
import os
import cmd_list


t0 = time.perf_counter()

robot_state.current_state = robot_state.FIRST_MOVE

while True:
    # Decide what over-riding state to be in.
    if time.perf_counter() > (t0+120):
        dead_stop()
    elif time.perf_counter() > (t0+90):
        robot_actions.move_to_home()
    elif (robot_state.current_state == robot_state.NULL) and (time.perf_counter() > (t0+20)):
        robot_state.current_state = robot_state.FIRST_MOVE

    # Act on the stats with current state
    if robot_state.current_state == robot_state.FIRST_MOVE:
        robot_actions.first_move()
        robot_state.current_state = robot_state.ROAM
    elif robot_state.current_state == robot_state.ROAM:
        robot_actions.roam()

    print(time.perf_counter() - t0)
    # Perform the action for that state.