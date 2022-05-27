// DEBUG is used when attached to serial monitor 
#define DEBUG false

void setup() {
  Serial.begin(115200);
  while (!Serial) {
    ; // wait for native USB implementation 
  }

  sendHelo();
  sendDebug("sent from sim-rig");
}

void loop() {

  sendHelo();
  sendDebug("in loop");
  // sendAck(P_ACK_OK);
  // sendAck(P_ACK_PARAMETER_ERROR);
  // sendAck(P_ACK_WRONG_CHECKSUM);
  // sendAck(P_ACK_NOT_INTERFACE_MODE);
  
  delay(200);
  
}
