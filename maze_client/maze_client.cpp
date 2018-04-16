#include <Arduino.h>
#include <Adafruit_ILI9341.h>
#include <SD.h>
#include "consts_and_types.h"
#include "map_drawing.h"
uint16_t x_prime;
uint16_t y_prime;
uint16_t size = 26; // size changes later
// as mentioned in README we ran into weird cases where the key input part of
// the code will get stuck in a loop. Changing the intial sizes seems to help
// and once it is working you can change it back and it will work fine
shared_vars shared;
Adafruit_ILI9341 tft = Adafruit_ILI9341(clientpins::tft_cs, clientpins::tft_dc);
void setup() {
  // initialize Arduino
  // NOTE we kept a lot of the files that were in assignment 1 in here since
  // they worked and we didn;t want to change something that wasn't broken
  init();
  // Not needed at all. Kind of forgot about this here and a little scared to
  // remove them because I am not near a VM to try out my code for the arduino
  pinMode(clientpins::zoom_in_pin, INPUT_PULLUP);
  pinMode(clientpins::zoom_out_pin, INPUT_PULLUP);
  pinMode(clientpins::joy_button_pin, INPUT_PULLUP);
  shared.joy_centre = xy_pos(analogRead(clientpins::joy_y_pin), analogRead(clientpins::joy_x_pin));
  // initialize serial port
  Serial.begin(9600);
  tft.begin();
  Serial.flush();  // get rid of any leftover bits
  tft.fillScreen(0x001F); // gives the lcd an intial blue screen
}

void draw_maze(){
  // This is the essential part of our code. This communicates betweent the
  // python server and the cpp client.
  // State functions to cycle through different parts of our communication
  // A line will be sent from the server of the maze and this part of the
  // code will draw the maze. It runs pretty fast but the larger the maze the
  // slower it will be
  enum State {ready_for_maze, waiting_for_line, ending};
  State curr_state = ready_for_maze;
  int16_t x = 0;
  int16_t y = 0;
  char incomingByte;
  while(true){
    Serial.flush();
    while (Serial.available() == 0);
    if (curr_state == ending){
      //Ending state that will send a comfirmation to server that it is moving on
      Serial.print("Q");
      Serial.flush();
      break;
    }
    if (curr_state == waiting_for_line){
      //Waits for the incoming lines of the maze.
      //Server will send a confirmation key to indicate that it is done sending
      incomingByte = Serial.read();
      if (incomingByte == '\n') {
        //new line indicates a new line of the maze
        Serial.print("Q");
        y += size;
        x = 0;
      }
      if (incomingByte == -1) continue;
      if (incomingByte == '%') continue;

      if (incomingByte == '1') {
        // based on the size of the maze we will change the size of the lcd maze to fit
        // changing this values to something small seems to help when we get caught in
        // the input key loop
        size = 16;
        y = -16;
        continue;
      }
      if (incomingByte == '9') {
        size = 26;
        y = -26;
        continue;
      }
      if (incomingByte == '2') {
        size = 9;
        y= -9;
        continue;
      }
      if (incomingByte == '5') {
        size = 4;
        y= -4;
        continue;
      }

      if (incomingByte == 'W') {
        // Indicates a wall
        tft.fillRect(x, y, size, size, 0x0000);
        x += size;
        continue;
      }
      if (incomingByte == 'P') {
        // Indicates a path
        tft.fillRect(x, y, size, size, 0xFFFF);
        x += size;
        continue;
      }
      if (incomingByte == 'S'){
        // Indicates the start position. Hard to see cause the cursor is drawn
        // over very quickly
        tft.fillRect(x, y, size, size, 0x00FF00);
        x_prime = x;
        y_prime = y;
        x += size;
        continue;
      }
      if (incomingByte == 'F'){
        // Finish line
        tft.fillRect(x, y, size, size, 0xF000);
        x += size;
        continue;
      }
      if (incomingByte == 'O'){
        // all the maze has been sent
        curr_state == ending;
        break;
      }

    }
    if (curr_state == ready_for_maze){
      // start of the handshaking part. Arduino is ready to recieve
      Serial.print("S");
      curr_state = waiting_for_line;
    }
  }
}

void move_cursor(){
  // This will constantly communicate with the server to update cursor postion
  // based on what the server sends. it will run until it recieves the end key.
  // This is where we typically get stuck in a loop and input keys won't work.

  // this works by drawing a light green square where the cursor was and a dark
  // green cursor in it's new place
  // this also gives the maze the nice and intentional trailing effect
  char incomingByte;
  uint16_t x = x_prime;
  uint16_t y = y_prime;
  while(true){
    Serial.flush();
    while (Serial.available() == 0);  //NOTE Gets stuck here sometimes :/
    incomingByte = Serial.read();
    Serial.print("*"); // print to arduino to let it know it is read to recieve
    if (incomingByte == 'R'){
      // move cursor right
      tft.fillRect(x, y, size, size, 0xFFF0);
      x += size;
      tft.fillRect(x, y, size, size, 0x0FF0);
      while (Serial.read() != 'Q');
    }
    else if (incomingByte == 'L'){
      // move cursor left
      tft.fillRect(x, y, size, size, 0xFFF0);
      x -= size;
      tft.fillRect(x, y, size, size, 0x0FF0);
      while (Serial.read() != 'Q');
    }
    else if (incomingByte == 'U'){
      // move cursor up
      tft.fillRect(x, y, size, size, 0xFFF0);
      y -= size;
      tft.fillRect(x, y, size, size, 0x0FF0);
      while (Serial.read() != 'Q');
    }
    else if (incomingByte == 'D'){
      // move cursor down
      tft.fillRect(x, y, size, size, 0xFFF0);
      y += size;
      tft.fillRect(x, y, size, size, 0x0FF0);
      while (Serial.read() != 'Q');
    }
    else if (incomingByte == 'O'){
      // ends the maze and breaks the loop
      while (Serial.read() != 'Q');
      break;
    }
    Serial.flush();
  }
}


int main() {
  setup();
  while (true) {
    // forever loop that lets the server play games for ever if you wanted to
    // without the need to re run the code or reset the Arduino
    // liekly you may still need to do so but ideally not
    tft.fillScreen(0x001F);
    // LET's start was a good indicator for us to know where the arduino was
    // within the code from the terminal
    Serial.println("LETS START");
    draw_maze();
    Serial.flush();
    move_cursor();
    Serial.flush();
  }
}
