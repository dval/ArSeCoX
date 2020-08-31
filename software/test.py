#!/usr/bin/python3
import sys
import COMCore

print("Starting ...")
print(sys.version)

link = COMCore.COMCore()

def testConnect():
        #get list of ports
        myPorts = link.listPorts()
        portSelect = input("Please enter number of test port: ")
        port_i = int(portSelect)-1

        #set port
        print ("Testing port: ", myPorts[int(portSelect)-1])
        link.setPort(port_i)

        #test connection
        link.open()
        # check for waiting data
        while link.connection.in_waiting:
            rez = link.read(64).decode('utf-8')
            print(rez)


        #send request id message
        ron = link.writeMessage("hello,1,0.1")
        print ("Sent handshake of %d bytes." % ron)
        # read 64 byte response
        #rez = link.read(64).decode('utf-8')
        rez = link.readMessage()
        # cleanup
        #link.close()
        return str(rez)


print ("Expecting: Port reset response.")
test_resetUI = link.reset()
print (test_resetUI)

print

print ("Expecting: Port list of n length")
#test_portlist = tec.autoConnect()
test_portlist = link.listPorts()
#formatted display for list in terminal
det = [' - '.join([str(test_portlist.index(p)+1), p.device, p.device_path, p.description,
 p.hwid, p.usb_description(), p.usb_info() ]) for p in test_portlist]
print(''+'\n'.join(map(str,det)))



print
connectStatus = testConnect()
print ("Expecting: Hardware response with 'callback' message.")
print ("Response: ", connectStatus)

print

"""
print ("Expecting: 3 formatted messages about sensor state.")
tec.comlink.open()
for m in range(3):
    print (str(m+1),'- ',tec.comlink.readMessage())
#tec.comlink.close()

print

print ("Expecting: some result from a callback?")
print (tec.getSensors())
print (tec.comlink.readMessage())
print (tec.comlink.readMessage())
print (tec.comlink.readMessage())
"""