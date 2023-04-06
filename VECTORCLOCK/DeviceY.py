from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer
import threading
from jsonrpclib import Server
from Vectorclock import Vectorclock

YVector = [0,0,0] 

#This thread listen to Messages
def listen(incv,incm):
    global YVector
    print("Before device Y Receiving a Message")
    print(YVector)
    #Maximum of two vectors are taken elementwise 
    YVector  = list(map(max, zip(YVector, incv)))
    YVector[1]=YVector[1]+1
    print("After device Y Receiving a Message - message: ",incm)
    print(YVector)
    
#This thread sends message to devices
def sendmes():
    deviceX = Server('http://localhost:8873')
    deviceZ = Server('http://localhost:8875')
    while True:
        dm = input("Enter message : ")
        dn = int(input("Enter Device Number to send (X:1,Y:2,Z:3) : "))
        if dn == 2: ## If Internal Event happens my method is called
            listen(YVector,dm)

        if dn == 1: ## Send Message to Device X
            print("Before device Y Sending a Message - message: ",dm)
            print(YVector)
            YVector[1]=YVector[1]+1
            deviceX.listen(YVector,dm)
            print("After device Y Sending a Message")
            print(YVector)

        if dn == 3:  ##Send Message to Device Z
            print("Before device Y Sending a Message - message: ",dm)
            print(YVector)
            YVector[1]=YVector[1]+1
            deviceZ.listen(YVector,dm)
            print("After device Y Sending a Message")
            print(YVector)

#Creating the RPC Server for the Device Y
localhost = '127.0.0.1'
deviceY = SimpleJSONRPCServer(('localhost', 8874))
th1 = threading.Thread(target=sendmes, args=())
th1.start()
deviceY.register_function(listen)
print("device Y is Up and Running")
#calling vectorclock class
clock = Vectorclock() 
YVector = [clock.getDeviceXTime(), clock.getDeviceYTime(), clock.getDeviceZTime()]
print("Device Y's Current Vector is: ",YVector)
deviceY.serve_forever()





