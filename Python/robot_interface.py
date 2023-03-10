import godot_interface
import vision
import camera
import settings
import cmd_list
import serial

if settings.USE_SERIAL:
    ser = serial.Serial(settings.SERIAL_PORT)  # “9600,8,N,1”


def turn_left():
    send_command(cmd_list.CMD_LEFT)


def turn_right():
    send_command(cmd_list.CMD_RIGHT)


def turn_stop():
    send_command(cmd_list.CMD_CENTRE)


def move_forward():
    send_command(cmd_list.CMD_FORWARD)


def move_backward():
    send_command(cmd_list.CMD_BACKWARD)


def move_stop():
    send_command(cmd_list.CMD_STOP)


def send_command(command):
    if settings.USE_SIM:
        godot_interface.send_command(command)

    if settings.USE_SERIAL:
        ser.write(str.encode(command))


def get_image():
    if settings.USE_SIM_CAMERA:
        png_image = godot_interface.get_image()
        return vision.robot_to_cv_image(png_image)
    else:
        return camera.get_image()
