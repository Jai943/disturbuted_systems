from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer
import threading
from jsonrpclib import Server
from Vectorclock import Vectorclock

ZVector = [0,0,0]

#isten to Messages using threads
def listen(incv,incm):
    global ZVector
    print("Before device Z Receiving a Message")
    print(ZVector)
    #Maximum of two vectors are taken elementwise 
    ZVector  = list(map(max, zip(ZVector, incv)))
    ZVector[2]=ZVector[2]+1
    print("After device Z Receiving a Message - message: ",incm)
    print(ZVector)
    
#sends message to devices using thread
def sendmes():
    deviceX = Server('http://localhost:8873')
    deviceY = Server('http://localhost:8874')
    while True:
        dm = input("Enter message : ")
        dn = int(input("Enter Device Number to send (X:1,Y:2,Z:3) : "))
        if dn == 3: ## if it sends to itself
            listen(ZVector,dm)
        if dn == 1: ## Send Message to Device X
            print("Before device Z Sending a Message - message: ",dm)
            print(ZVector)
            ZVector[2]=ZVector[2]+1
            deviceX.listen(ZVector,dm)
            print("Vector clock After device Z Sending a Message")
            print(ZVector)

        if dn == 2:  ##Send Message to Device Y
            print("Before device Z Sending a Message - message: ",dm)
            print(ZVector)
            ZVector[2]=ZVector[2]+1
            deviceY.listen(ZVector,dm)
            print("After device Z Sending a Message")
            print(ZVector)

#RPC using JSON - for DEVICE Z
deviceZ = SimpleJSONRPCServer(('localhost', 8875))
th1 = threading.Thread(target=sendmes, args=())
th1.start()
deviceZ.register_function(listen)
print("device Z is Up and Running")
#calling vectorclock class
clock = Vectorclock() 
ZVector = [clock.getDeviceXTime(), clock.getDeviceYTime(), clock.getDeviceZTime()]
print("Device Z's Current Vector is: ",ZVector)
deviceZ.serve_forever()
