import godot_interface
import vision
import camera
import settings
import cmd_list
import serial
import robot_state
import time

if settings.USE_SERIAL:
    ser = serial.Serial(settings.SERIAL_PORT, 9600, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE, 0.01)


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


def check_collision():
    send_command(cmd_list.CMD_CHECK_COLLISION + str(" ") + str(settings.SENSOR_ID_LEFT))
    time.sleep(0.1)
    send_command(cmd_list.CMD_CHECK_COLLISION + str(" ") + str(settings.SENSOR_ID_RIGHT))
    time.sleep(0.1)
    send_command(cmd_list.CMD_CHECK_COLLISION + str(" ") + str(settings.SENSOR_ID_BACK))
    time.sleep(0.1)

def process_collision_response(str):
    s = str.split(" ")
    if (s[0] != cmd_list.CMD_CHECK_COLLISION):
        return

    id = s[1]
    if s[2] == '0':
        state = False
    else:
        state = True
    
    if(id == settings.SENSOR_ID_LEFT):
        robot_state.collision_left = state
    elif(id == settings.SENSOR_ID_RIGHT):
        robot_state.collision_right = state
    elif (id == settings.SENSOR_ID_BACK):
        robot_state.collision_back = state


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

        if settings.DEBUG_SHOW_SERIAL:
            print(line)

        if(line[0] == cmd_list.CMD_CHECK_COLLISION):
            process_collision_response(line)
        elif(line[0] == cmd_list.CMD_RESET):
            robot_state.reset_flag = True
    except:
        line = ""

    return line

def get_image():
    if settings.USE_SIM_CAMERA:
        png_image = godot_interface.get_image()
        return vision.sim_to_cv_image(png_image)
    else:
        return camera.get_image()
