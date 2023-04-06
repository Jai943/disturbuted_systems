from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer
import threading
from jsonrpclib import Server
from Vectorclock import Vectorclock

XVector = [0,0,0] 

#listen to Messages using threads
def listen(incv,incm):
    global XVector
    print("Before device X Receiving a Message")
    print(XVector)
    #Maximum of two vectors are taken elementwise 
    XVector  = list(map(max, zip(XVector, incv)))
    XVector[0]=XVector[0]+1
    print("After device X Receiving a Message - message: ",incm)
    print(XVector)
    
# sends message to devices using thread
def sendmes():
    deviceY = Server('http://localhost:8874')
    deviceZ = Server('http://localhost:8875')
    while True:
        dm = input("Enter message : ")
        dn = int(input("Enter Device Number to send (X:1,Y:2,Z:3) : "))
        if dn == 1: ## if it sends to itself
            listen(XVector,dm)

        if dn == 2: ## Send Message to Device Y
            print("Before device X Sending a Message - message: ",dm)
            print(XVector)
            XVector[0]=XVector[0]+1
            deviceY.listen(XVector,dm)
            print("After device X Sending a Message")
            print(XVector)

        if dn == 3:  ##Send Message to Device Z
            print("Before device X Sending a Message - message: ",dm)
            print(XVector)
            XVector[0]=XVector[0]+1
            deviceZ.listen(XVector,dm)
            print("After device X Sending a Message")
            print(XVector)


#RPC using JSON - for DEVICE X
localhost = '127.0.0.1'
deviceX = SimpleJSONRPCServer(('localhost', 8873))
th1 = threading.Thread(target=sendmes, args=())
th1.start()
deviceX.register_function(listen)
print("device X is Up and Running")
#calling vectorclock class
clock = Vectorclock() 
XVector = [clock.getDeviceXTime(), clock.getDeviceYTime(), clock.getDeviceZTime()]
print("Device X's Current Vector is: ",XVector)
deviceX.serve_forever()



