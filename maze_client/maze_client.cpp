#include <Arduino.h>
#include <Adafruit_ILI9341.h>
#include <SD.h>
#include "consts_and_types.h"
#include "map_drawing.h"

// the variables to be shared across the project, they are declared here!
shared_vars shared;

Adafruit_ILI9341 tft = Adafruit_ILI9341(clientpins::tft_cs, clientpins::tft_dc);

void setup() {
  // initialize Arduino
  init();

  // initialize zoom pins
  pinMode(clientpins::zoom_in_pin, INPUT_PULLUP);
  pinMode(clientpins::zoom_out_pin, INPUT_PULLUP);

  // initialize joystick pins and calibrate centre reading
  pinMode(clientpins::joy_button_pin, INPUT_PULLUP);
  // x and y are reverse because of how our joystick is oriented
  shared.joy_centre = xy_pos(analogRead(clientpins::joy_y_pin), analogRead(clientpins::joy_x_pin));
  // initialize serial port
  Serial.begin(9600);
  tft.begin();
  Serial.flush(); // get rid of any leftover bits
  // initially no path is stored
  tft.fillScreen(0xF008);
}



void draw_maze(){
  // This is the essential part of our code. This communicates betweent the
  // python server and the cpp client.
  //State functions to cycle through different parts of our communication
  enum State {ready_for_maze, waiting_for_line, ending};
  State curr_state = ready_for_maze;
  uint16_t x = 0;
  uint16_t y = 0;
  char incomingByte;
  while(true){
    while (Serial.available() == 0);
    if (curr_state == ending){
      // this is the last part of the communication. We break outta loop and
      // continue on to the drawing part of this code.
      // we could have a check somewhere else to make sure server is sending
      // 'E' as a confirmation of all the waypoints have been sent.
      // The server is sending this but since everything is working it seems
      // redundant to this now

      Serial.flush();
      break;
    }
    if (curr_state == waiting_for_line){

      incomingByte = Serial.read();
      if (incomingByte == '\n') {
        Serial.print("Q");
        y += 5;
        x = 0;
      }
      if (incomingByte == -1) continue;
      if (incomingByte == '%') continue;
      if (incomingByte == 'W') {
        tft.fillRect(x, y, 5, 5, 0x0000);
        x += 5;
        continue;
      }
      if (incomingByte == 'P') {
        tft.fillRect(x, y, 5, 5, 0xFFFF);
        x += 5;
        continue;
      }
      if (y==210){
        curr_state == ending;
        break;
      }

    }
    if (curr_state == ready_for_maze){
      Serial.print("S");
      curr_state = waiting_for_line;
    }
  }
}

void move_cursor(){
  char incomingByte;
  uint16_t x = 5;
  uint16_t y = 5;
  tft.fillRect(x, y, 5, 5, 0x001F);
  while(true){
    while (Serial.available() == 0);
    incomingByte = Serial.read();
    if (incomingByte == 'R'){
      tft.fillRect(x, y, 5, 5, 0xFFFF);
      x += 5;
      tft.fillRect(x, y, 5, 5, 0x001F);
    }
  }
}

int main() {
  setup();
  Serial.println("LETS START");
  draw_maze();

  Serial.flush();
  while (true) {
    Serial.print("T");
  }
}
