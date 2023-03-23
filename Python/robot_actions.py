import time

import robot_state
import settings
import robot_interface as rb
import vision
from random import randrange


def first_move():
    rb.gate_open()
    turn_degree(45)
    move_forward_m(0.75)
    turn_degree(135)


def roam():
    rand_ang = (randrange(5) - 2)*45
    print(rand_ang)
    turn_degree(rand_ang)
    rb.check_collision()
    time.sleep(0.5)
    if(not robot_state.collision_left) and (not robot_state.collision_right):
        rb.gate_open()
        time.sleep(0.5)
        move_forward_m(0.1)
    elif(not robot_state.collision_back):
        rb.gate_shut()
        time.sleep(0.5)
        move_back_m(0.1)
    else:
        rb.flash_LED()

# Search for a tag and move the robot towards it
def move_to_tag(index):
    for i in range(12):
        image = rb.get_image()
        vision.image_process(image)

        rb.check_collision()

        if vision.tag_visible(index):
            if (not robot_state.collision_left) and (not robot_state.collision_right):
                move_forward_m(0.25)
            else:
                rb.flash_LED()
        else:
            turn_degree(30)


# Go to the starting position
def move_to_home():
    move_to_tag(settings.HOME_TAG)


def move_forward_m(distance_m):
    rb.gate_open()
    time.sleep(0.25)
    rb.move_forward()
    time.sleep(distance_m * settings.TIME_1M)
    dead_stop()


def move_back_m(distance_m):
    rb.gate_shut()
    rb.move_backward()
    time.sleep(distance_m * settings.TIME_1M)
    dead_stop()


def turn_degree(angle):  #+ is left, - is right
    rb.gate_shut()
    if angle > 0:
        rb.turn_left()
    elif angle < 0:
        rb.turn_right()

    time.sleep((abs(angle)/360)*settings.TIME_360_DEGREE)
    dead_stop()


def dead_stop():
    rb.turn_stop()
    rb.move_stop()
    time.sleep(0.1)
