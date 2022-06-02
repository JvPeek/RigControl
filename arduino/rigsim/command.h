#include <Arduino.h>  //needed for Serial.println()


const uint8_t C_INIT = 0x01;
const uint8_t C_HELO = 0x74;
const uint8_t C_DEBUG = 0xfe;
const uint8_t C_ACK = 0xf0;
const uint8_t P_ACK_OK = 0x00;
const uint8_t P_ACK_PARAMETER_ERROR = 0x01;
const uint8_t P_ACK_WRONG_CHECKSUM = 0x02;
const uint8_t P_ACK_NOT_INTERFACE_MODE = 0x03;

struct RecievedCommand {
   uint8_t type;
   uint8_t id;
   uint8_t payloadLength;
   uint8_t payload[8];
   uint8_t checksum;
};


void sendCommand(uint8_t command, uint8_t packetCount, uint8_t* payload = 0, int payloadSize = 0);

void sendHelo(void);
void sendDebug(char* string);
void sendAck(uint8_t packetId, uint8_t ackType = C_ACK);
void sendInit(uint8_t packetId, uint8_t ackType = C_ACK, uint8_t versionMajor = 0x00, uint8_t versionMinor = 0x02);

RecievedCommand readCommand();