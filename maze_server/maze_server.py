from time import sleep
from serial import Serial
import numpy as np


def wait_for_confirmation():
    with Serial("/dev/ttyACM0", baudrate=9600, timeout=0.1) as ser:
        while True:
            line = ser.readline()
            line_string = line.decode("ASCII")
            stripped = line_string.rstrip("\r\n")
            if stripped == 'Q':
                break
            else:
                print('Waiting for Q got: ', stripped)

            sleep(2)


def send_maze(file):
    '''
        receive data from arduino

        This function is intended to loop forever without a break.
        this has no state function unlike the client.
        If something happens with the communication that breaks the
        handshaking process then it is up to the client to get back to the
        right state and send start and end points over here so the server can
        reconstruct a new path
    '''
    with Serial("/dev/ttyACM0", baudrate=9600, timeout=0.001) as ser:
        while True:
            line = ser.readline()
            if not line:
                print("timeout, restarting...")
                continue
            line_string = line.decode("ASCII")
            stripped = line_string.rstrip("\r\n")
            print(stripped)
            if stripped[0] == 'S':   # S indicates the start of the maze gen.
                for l in file:
                    print(l)
                    encoded = l.encode("ASCII")
                    ser.write(encoded)
                    wait_for_confirmation()

            else:
                out_line = "%"
                encoded = out_line.encode("ASCII")
                ser.write(encoded)
            sleep(2)
    return 0

def send_movement():
    '''

        takes user input.
        validates input.
        sends input.
    '''
    while True:
        blank_image = np.zeros((500, 500, 3), np.uint8)





# if running this specific script, await user command
if __name__ == "__main__":
    file = open("test_maze_3.txt", "r")
    send_maze(file)
