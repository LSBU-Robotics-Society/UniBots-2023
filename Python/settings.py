
# Change this before the start of an event to tell the robot where the home position is
HOME_TAG = 0

USE_SIM = False  # This should be False when using the real robot
USE_SIM_CAMERA = False  # This should be False when using the real robot
USE_SERIAL = True  # Should usually be True, set False to disable Arduino communication

SERIAL_PORT = '/dev/ttyUSB0'  # The serial port used to communicate with the Arduino

SENSOR_ID_LEFT = '0'
SENSOR_ID_RIGHT = '1'
SENSOR_ID_BACK = '2'

# Simulator settings
SIM_WS_ADDRESS = "ws://localhost:9080"  # This is the address of the simulator

TIME_360_DEGREE = 1.5 # Time in seconds for a 360 degree turn.
TIME_1M = 1.7 #Time for 1 m of forward movement, ~60 cm in 1 second

DEBUG_SHOW_SERIAL = False