# final_project

This is our final project THE A-MAZING-Game

  We randomly generate a Maze of various sizes onto the ardunio LCD screen and the user must
  navigate through the maze using keyboard input via a python server.

  When code initially runs user must be on the main menu screen and press enter

  the maze will generate and display on the arduino.

  Staying in the new command window that prompts user to press input keys... press arrow keys to
  navigate the maze

  once you either reach the end goal indicated as a red square or press "ESC" on the keyboard the
  game will end and you will be taken to the end game screen

  to start a new game press s, m, l, x, S, M, L, X to start a new game at various sizes

  press esc from here to exit the program

In this project the Arduino acts as our client to display maze and user position
the server is our python code that generates and sends the maze to the client by first making
a text file of the maze.



Contributors:
Maxwell McEvoy 1288336
Nicholas Serrano 1508361

Arduino wiring instructions:

Wiring of adafruit display: from bottom to top on the right side (the side with the pins).

Board Pin <---> Arduino Pin
===========================
GND             GND
Vin             5V
3Vo             NOT CONNECTED
CLK             52
MISO            50
MOSI            51
CS              10
D/C             9
RST             NOT CONNECTED
Lite            NOT CONNECTED
Y+              A2 (analog pin)
X+              4  (digital pin)
Y-              5  (digital pin)
X-              A3 (analog pin)
IM0 - IM3       NOT CONNECTED (they expect a 3.3v signal, DON'T CONNECT!)
CCS             6
CD              NOT CONNECTED

How to run code:

  ensure opencv is install please do so for the VM with the following entry into the terminal

  'sudo pip3 install opencv-python'

  'make upload' while in the maze_client directory
  'python3 maze_server.py' or 'python3 maze_server_backup.py' within the maze_server directory

Please Note:
  This project was intended for the arduino and a demo of it working can be viewed with the link
  below. There was a problem that occured with the handshaking component. It was hard to find out
  what the problem was. It would work perfectly one day and I'd save my code. Then I would test it again
  on a differnet machine and it wouldn't work until i did some arbitrary tweaking.
  If it works it works amazing but if it doesn't it just won't

  If the arduino is not working for you please try the maze_server_backup.py file. It was hastily
  put together but displays what we did well enough to show you the functions of the maze generation
  and user input movement. The display is a little off sorry.

  https://drive.google.com/open?id=14zTCWnVFy-CdcyBsBYnoBmhNyKWejsQ1
