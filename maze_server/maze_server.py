from time import sleep
from serial import Serial
import numpy as np
import cv2
import MazeGen


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
                    maze_array.append(l)

                    # wait_for_confirmation()  #TODO Not working
                o = "O"
                encoded = o.encode("ASCII")
                ser.write(encoded)
                return maze_array
            else:
                out_line = "%"
                encoded = out_line.encode("ASCII")
                ser.write(encoded)
            sleep(2)


def validate_movement(input_key, x, y, maze_array):
    '''
        this will validate the keys entered to ensure it is a valid move
        if it is the move will be sent to the arduino and the lcd will update
        else nothing will happen and it will return

        Input:
            input_keys
                0x51 left
                0x52 up
                0x53 right
                0x54 left
            current_location
                depending on how we store this we will read the location
                of the cursor on the lcd
        Returns:
            updated current_location
    '''
    valid = False
    if (input_key == "D") and (y != size-1):  # down arrow keys
        if maze_array[y+1][x] != "W":
            valid = True
            y += 1
    elif input_key == "R" and (x != size-1):  # right arrow key
        if maze_array[y][x+1] != "W":
            valid = True
            x += 1
    elif input_key == "U" and (y != 0):  # up arrow keys
        if maze_array[y-1][x] != "W":
            valid = True
            y -= 1
    elif input_key == "L" and (x != 0):  # left arrow keys
        if maze_array[y][x-1] != "W":
            valid = True
            x -= 1
    elif input_key == "O":
        valid = True

    # TODO check if movement is valid based on current_location
    # print(input_key, "Here")
    if valid:
        with Serial("/dev/ttyACM0", baudrate=9600, timeout=0.001) as ser:
            k = input_key
            encoded = k.encode("ASCII")
            ser.write(encoded)
            while True:
                ser.write(encoded)
                line = ser.readline()
                if not line:
                    # print("waiting")
                    continue
                line_string = line.decode("ASCII")
                stripped = line_string.rstrip("\r\n")
                # print(stripped)
                if stripped[0] == 'S':
                    q = 'Q'
                    encoded = q.encode("ASCII")
                    ser.write(encoded)
                    break
                sleep(3)
    return x, y


def title_screen(file, maze_array):
    '''

        takes user input.
        validates input.
        sends input.

        sudo pip3 install opencv-python

    '''
    font = cv2.FONT_HERSHEY_SIMPLEX
    title_text = "Maze Game"
    enter_text = "Press Enter to generate maze"
    key_text = "Press arrow keys to move"
    escape_text = "Pres Esc to exit"
    over_text = "Game is over pls play again"

    title = np.zeros((800, 1500, 3), np.uint8)
    cv2.putText(title, title_text, (350, 100), font, 4,
                (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(title, enter_text, (250, 500), font, 2,
                (255, 255, 255), 2, cv2.LINE_AA)
    cv2.imshow("A-MAZE-ING GAME", title)
    cv2.moveWindow("A-MAZE-ING GAME", 0, 0)
    once = True
    x, y = 0, 0
    while True:
        input_key = cv2.waitKey(0) & 0xFF
        if input_key == 0x0D and once:
            maze_array = send_maze(file)
            cv2.destroyAllWindows()
            title = np.zeros((800, 1500, 3), np.uint8)
            cv2.putText(title, title_text, (350, 100), font, 4,
                        (255, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(title, key_text, (270, 500), font, 2,
                        (255, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(title, escape_text, (0, 780), font, 1,
                        (255, 255, 255), 2, cv2.LINE_AA)
            once = False
        cv2.imshow("A-MAZE-ING GAME", title)
        cv2.moveWindow("A-MAZE-ING GAME", 0, 0)

        if input_key == 0x54:  # down arrow keys
            # print("D")
            x, y = validate_movement("D", x, y, maze_array)
        if input_key == 0x53:  # right arrow key
            # print("R")
            x, y = validate_movement("R", x, y, maze_array)
        if input_key == 0x52:  # up arrow keys
            # print("U")
            x, y = validate_movement("U", x, y, maze_array)
        if input_key == 0x51:  # left arrow keys
            # print("L")
            x, y = validate_movement("L", x, y, maze_array)
        if input_key == 0x1B:  # escape
            x, y = validate_movement("O", x, y, maze_array)
            break

    title = np.zeros((800, 1500, 3), np.uint8)
    cv2.circle(title, (400, 750), 1500, (0, 0, 255), -1)
    cv2.putText(title, over_text, (70, 400), font, 3,
                (255, 255, 255), 2, cv2.LINE_AA)
    cv2.imshow("A-MAZE-ING GAME", title)
    cv2.moveWindow("A-MAZE-ING GAME", 0, 0)
    cv2.waitKey(0)


if __name__ == "__main__":
    size = 27
    MazeGen.maze_gen(size)
    file = open("sendfile.txt", "r")
    g = file
    maze_array = []

    title_screen(g, maze_array)
