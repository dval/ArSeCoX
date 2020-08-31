#!/usr/bin/python3
'''
MIT License

Copyright (c) 2019 Dylan Valentine

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''


import serial
import serial.tools.list_ports

'''
Responsable for communicating with hardware over serial connection. COMCore 
should be able to search all COM ports for hardware ID and automatically
connect to the correct one. If it is unable to find the expected hardware ID,
then it can provide a list of active COM ports to manually select from.

COMCore also handles the packing, sending, receiving, unpacking of message
packets sent to and from the device. This gives a human-readable set of 
commands that can be displayed or logged for trouble-shooting.
'''
class COMCore(object):
    """docstring for COMCore."""

    connection = serial.Serial()

    def __init__(self):
        super(COMCore, self).__init__()
        self.connection.baudrate = 19200
        self.connection.timeout = 8
        self.connection.rtscts = 1

    def listPorts(self):
        #list of COM ports available
        ports = serial.tools.list_ports.comports(include_links=True)
        return ports

    def setPort(self, p_index):
        #set specific port
        self.connection.port = self.listPorts()[p_index].device

    def open(self):
        #make serial connection to port
        self.connection.open()
        return

    def close(self):
        #close serial connection
        self.connection.close()
        return True

    def reset(self):
        #TODO: whatever this is trying to do, it's not working.
        # Find some way to store last connected port and PID.
        # On new connection attempt, if the desired port is not found,
        # then kill old PID and check port again. (or find PID associated
        # with desired port, and kill it.)
        result = "Error"
        if(self.connection.is_open):
            self.connection.close()
            self.connection.reset_input_buffer()
            self.connection.reset_output_buffer()
            result = "Port reset. Ready to open."
        elif(not self.connection.is_open):
            result = "No port is open to reset."
        return result

    def read(self, bytes):
        '''read number of bytes from port stream'''
        packet = self.connection.read(bytes)
        return packet

    def write(self, data):
        '''Accepts string and sends it as serial packet(s).'''
        packetSize = self.connection.write(data.encode('utf-8'))
        return packetSize


    def readMessage(self):
        '''Reads the incoming packet and returns to a string.'''
        startMarker = ord('<')  #char 60     #start character of message packet
        endMarker = ord('>')    #char 62       #end character of message packet
        packet = ""             #complete message
        checkChar = "1"         #anything not the startMarker
        # wait for the start character
        while  ord(checkChar) != startMarker:
            checkChar = self.read(1)
        #data to packet until the end marker is found
        while ord(checkChar) != endMarker:
            if ord(checkChar) != startMarker:
                packet = packet + checkChar.decode('utf-8')
            checkChar = self.read(1)
        #return the completed packet
        return packet

    def writeMessage(self, data):
        '''Write data to serial stream.'''
        packet = "<"
        packet = packet + data
        packet = packet + ">\n\r"
        packetSize = self.write(packet)
        return packetSize
