#include "SerialPacket.h"

// stream state
boolean readInProgress = false;
boolean writeInProgress = false;
boolean firstRun = true;

// input buffer
char inputBuffer[buffSize]; // this is the msg of the packet
byte bytesRecvd = 0;
char currentCommand[] = {};

// output buffer
char sendBuffer[buffSize]; // this is msg of the packet
int bytesSent = 0;

// initalize blank templates
_Packet incoming_packet;
_Packet outgoing_packet;
_Packet blank_packet;

// check the outgoing buffer, and if data is available, 
// set writing state and move data to outgoing packet.
void packData(){
  
  // if buffer is empty,
  if(sizeof(sendBuffer)<3){
    // build empty packet
    outgoing_packet.msgLength = 0;
    const char *endit = "\0";
    strcpy(outgoing_packet.msg, endit);
    
  }else{
    // write current buffer to outgoing packet
    // _Packet msg = <"callback",0,0.0>
    outgoing_packet.msgLength = sizeof(sendBuffer);
    strcpy(outgoing_packet.msg, "<");
    strcat(outgoing_packet.msg, sendBuffer);
    strcat(outgoing_packet.msg, ">"); 
    
  }
}

// checks the incoming buffer, and if data is available, 
// handles reading and routing of incoming messages
void unpackData(char msg[]) {
  
  // split the data into its parts
  char * strtokIndx;                      // c++ magic
  strtokIndx = strtok(msg, ", ");         // get the first part - the string
  //this is the 'handshake' command
  if (strcmp(strtokIndx,"hello")==0) {
    // continue parsing
    strtokIndx = strtok(NULL, ",");
    int p = atoi(strtokIndx);
    strtokIndx = strtok(NULL, ">");
    float q = atof(strtokIndx);
    // finally
    callback( "I received the following:  ", p, q );
    
  }else if (strcmp(strtokIndx,"fan")==0) {
    char p[]={'\0'};
    strcpy(p,strtok(NULL,","));
  }
 
  delete [] strtokIndx;
}

// Send packet as string and then clear buffer.
void writeData() {
  
    writeInProgress = true;
    packData();
    // if not reading
    //if (!readInProgress) {
      
      // send packet
      Serial.println(outgoing_packet.msg);
  
      // clear outgoing packet
      outgoing_packet = blank_packet;
      strcpy(sendBuffer, "\n"); 
      writeInProgress = false;
    //}
}

// reads available stream data into incoming buffer
// then sends the body of the message to parseData
void readData() {
  if (Serial.available() > 0) {
    char x = Serial.read();
    // The order of IFs is significant.
    // Assume we didn't start at the end
    if (x == endMarker){          
      inputBuffer[bytesRecvd] = 0;
      // after read is done, unpack data
      readInProgress = false;
      unpackData(inputBuffer);
    }
    if (readInProgress) {
      // read chars into buffer
      inputBuffer[bytesRecvd] = x;
      bytesRecvd ++;
      if (bytesRecvd == buffSize) {
        bytesRecvd = buffSize - 1;
      }}
    if (x == startMarker) {
      bytesRecvd = 0;
      readInProgress = true;}
  }//end if Serial.available
}//end readData


//================================//
// Things we can do.
// These are the commands that will 
// be called by the software, 
//================================//

// literal 'callback' function
void callback(String msg,int p, float q){
  
  // build data
  strcpy(sendBuffer, msg.c_str());
  //strcat(sendBuffer, ",");
  //strcat(sendBuffer, (char)p );
  //strcat(sendBuffer, ",");
  //strcat(sendBuffer, (char)q );
  // store data
  //strcpy(outgoing_packet.msg, sendBuffer);
  // move data
  //writeData();
}


void setup() {
  // take the com mr. sulu 
  // random picked baudrate         
  Serial.begin(19200);
  // let all things wake
  delay(250);

  // This is the 'hello' part of the 'handshake'
  // When the Arduino receives a 'hello' back,
  // it will then start listening for PC commands.
  
  // wait for host system to connect
  while(!Serial);
  // add data to buffer
  strcpy(sendBuffer, "COM Link Active. ");
  // copy buffer to packet
  strcpy(outgoing_packet.msg, sendBuffer);
  writeData();
  readData();
  
}

void loop() {
  // put your main code here, to run repeatedly:

  if(firstRun){
    firstRun = false;
      
    strcpy(sendBuffer, "System Ready.");     //tell the PC we are ready
    strcpy(outgoing_packet.msg, sendBuffer);

  }

  // if not currently writing, try
  // to read. if nothing to read, 
  // do some work, and write results.
  if( !writeInProgress){
    readData();
    if( !readInProgress ){
      // do stuff here
      writeData();
    }
  }
  
}
