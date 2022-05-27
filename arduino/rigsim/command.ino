
const uint8_t C_HELO = 0x74;
const uint8_t C_DEBUG = 0xfe;
const uint8_t C_ACK = 0xf0;
const uint8_t P_ACK_OK = 0x00;
const uint8_t P_ACK_PARAMETER_ERROR = 0x01;
const uint8_t P_ACK_WRONG_CHECKSUM = 0x02;
const uint8_t P_ACK_NOT_INTERFACE_MODE = 0x03;


void sendCommand(uint8_t command, uint8_t packetCount, uint8_t* payload = 0, int payloadSize = 0) {
  uint8_t packetSize = 4 + payloadSize; // (id + count + crc + length) + payloadSize
  uint8_t checksum = 0x00;

  checksum ^= command;
  checksum ^= packetCount;
  checksum ^= payloadSize;

#if DEBUG 
    Serial.print("Would send: "); Serial.print(command, HEX); Serial.print(", "); Serial.print(packetCount, HEX); Serial.print(", "); Serial.print(payloadSize, HEX); Serial.print(", ");
#else
    Serial.write(command);
    Serial.write(packetCount);
    Serial.write(payloadSize);
#endif

  for(uint8_t i = 0; i < payloadSize; i++) {
    checksum ^= payload[i];
    #if DEBUG 
      Serial.print(payload[i], HEX); Serial.print(", ");
    #else
      Serial.write(payload[i]);
    #endif
  }
  
  #if DEBUG
    Serial.print(checksum, HEX); Serial.println("");
  #else
    Serial.write(checksum);
  #endif
}

void sendHelo(void) {
  sendCommand(C_HELO, 0x00);
}

void sendDebug(char* string) {
  sendCommand(C_DEBUG, 0x00, string, strlen(string));
}

void sendAck(uint8_t packetCount, uint8_t ackType = P_ACK_OK) {
  uint8_t payload[] = {ackType};
  sendCommand(C_ACK, packetCount, payload, 1);
}

void readCommand() {
  uint8_t buffer = [256];
  uint8_t commandLength = 0;
}
