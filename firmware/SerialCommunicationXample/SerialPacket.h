#ifndef SerialPacket
#define SerialPacket
#include <Arduino.h>


// Some idea of stream management
#define buffSize 64           // should be adequate bytes for commands
#define startMarker '<'       // html style start/end tags as vars to 
#define endMarker '>'         // make parsing logic easier to read 


// using the same 'packet' template for both RX and TX
struct _Packet
{
  char msg[buffSize] = {};            // lazy using same size buffer in both directions
  int msgLength = 0;                  // number of bytes in the message
  //char status[42] = "000: No Status"; // readable status message for logging 42 bytes
};


#endif
