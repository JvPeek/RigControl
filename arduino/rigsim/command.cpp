#include "command.h"



uint8_t receivedCommandBuffer[256];

void sendCommand(uint8_t command, uint8_t packetCount, uint8_t* payload, int payloadSize) {
  uint8_t packetSize = 4 + payloadSize;  // (id + count + crc + length) + payloadSize
  uint8_t checksum = 0x00;

  checksum ^= command;
  checksum ^= packetCount;
  checksum ^= payloadSize;

#if DEBUG
  Serial.print("Would send: ");
  Serial.print(command, HEX);
  Serial.print(", ");
  Serial.print(packetCount, HEX);
  Serial.print(", ");
  Serial.print(payloadSize, HEX);
  Serial.print(", ");
#else
  Serial.write(command);
  Serial.write(packetCount);
  Serial.write(payloadSize);
#endif

  for (uint8_t i = 0; i < payloadSize; i++) {
    checksum ^= payload[i];
#if DEBUG
    Serial.print(payload[i], HEX);
    Serial.print(", ");
#else
    Serial.write(payload[i]);
#endif
  }

#if DEBUG
  Serial.print(checksum, HEX);
  Serial.println("");
#else
  Serial.write(checksum);
#endif
}

void sendHelo(void) {
  sendCommand(C_HELO, 0x00);
}

void sendDebug(char* string) {
  sendCommand(C_DEBUG, 0x00, (uint8_t*)string, strlen(string));
}

void sendAck(uint8_t packetId, uint8_t ackType) {
  uint8_t payload[] = { ackType };
  sendCommand(C_ACK, packetId, payload, 1);
}

void sendInit(uint8_t packetId, uint8_t ackType, uint8_t versionMajor, uint8_t versionMinor) {
  uint8_t payload[] = {
    ackType,
    versionMajor,  // Version Major
    versionMinor,  // Version Minor
    0x12,
    0x34,
    0x56,
    0x78
  };
  sendCommand(C_INIT, packetId, payload, 7);
}

RecievedCommand readCommand() {
  RecievedCommand command;
  uint8_t commandLength = 0;
  command.type = Serial.read();           // cmd
  command.id = Serial.read();             // PacketCount
  command.payloadLength = Serial.read();  // DataLength
  for (uint8_t i = 0; i < command.payloadLength; i++) {
    command.payload[i] = Serial.read();
  }
  command.checksum = Serial.read();  // Checksum

  return command;
}
