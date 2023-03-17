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


def gate_open():
    send_command(cmd_list.CMD_GATE_OPEN)


def gate_shut():
    send_command(cmd_list.CMD_GATE_SHUT)


def flash_LED():
    send_command(cmd_list.CMD_LED)


def send_command(command):
    if settings.USE_SIM:
        godot_interface.send_command(command)

    if settings.USE_SERIAL:
        try:
            ser.write(str.encode(command+'\r'+'\n'))
        except:
            return 0

def get_command():
    try:
        line = ser.readline()
        line = line.decode()
        line = line.strip()
    except:
        line = ""

    return line

def get_image():
    if settings.USE_SIM_CAMERA:
        png_image = godot_interface.get_image()
        return vision.robot_to_cv_image(png_image)
    else:
        return camera.get_image()
