from time import sleep
from serial import Serial


def wait_for_confirmation():
    with Serial("/dev/ttyACM0", baudrate=9600, timeout=0.1) as ser:
        while True:
            line = ser.readline()
            if not line:
                print("timeout, restarting...")
                continue
            line_string = line.decode("ASCII")
            stripped = line_string.rstrip("\r\n")
            # Q means line has been received and ready for next
            if stripped[0] == 'Q':
                break
            sleep(2)


def communication(file):
    '''
        receive data from arduino

        This function is intended to loop forever without a break.
        this has no state function unlike the client.
        If something happens with the communication that breaks the
        handshaking process then it is up to the client to get back to the
        right state and send start and end points over here so the server can
        reconstruct a new path
    '''
    with Serial("/dev/ttyACM0", baudrate=9600, timeout=0.1) as ser:
        while True:
            line = ser.readline()
            if not line:
                print("timeout, restarting...")
                continue
            line_string = line.decode("ASCII")
            stripped = line_string.rstrip("\r\n")

            if stripped[0] == 'S':   # S indicates the start of the maze gen.
                for l in file:
                    encoded = l.encode("ASCII")
                    ser.write(encoded)
                    wait_for_confirmation()
                    continue
            else:
                out_line = "%"
                encoded = out_line.encode("ASCII")
                ser.write(encoded)
            sleep(2)
    return 0


# if running this specific script, await user command
if __name__ == "__main__":
    file = open("test_maze.txt", "r")
    communication(file)
