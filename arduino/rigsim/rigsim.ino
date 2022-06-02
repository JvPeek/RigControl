// DEBUG is used when attached to serial monitor 
#define DEBUG false

#include "command.h"


void setup() {
  Serial.begin(115200);
  while (!Serial) {
    ; // wait for native USB implementation 
  }

  sendHelo();
  sendDebug("sent from sim-rig");
}



void loop() {
  if(Serial.available() > 0) {
    RecievedCommand receivedCommand = readCommand();
    switch(receivedCommand.type) {
      case 0x01: // INIT
        sendInit(receivedCommand.id, P_ACK_OK);
      default: 
        // sendAck(receivedCommand.id, P_ACK_PARAMETER_ERROR);
        sendDebug("unknown command type");
    }
  }

  // sendHelo();
  // sendDebug("in loop");
  // sendAck(P_ACK_OK);
  // sendAck(P_ACK_PARAMETER_ERROR);
  // sendAck(P_ACK_WRONG_CHECKSUM);
  // sendAck(P_ACK_NOT_INTERFACE_MODE);
  
  delay(200);
  
}
