import argparse,json
from sys import exit
from time import sleep
from socket import socket, AF_INET, SOCK_STREAM

host, port = '127.0.0.1',8054
address = (host, port)


SYNC = 0  #rpc code for sync is 0
ASYNC = 1  #rpc code for sync is 1

SYN = ACK = 1  #code for request 1
REQ = 2  #code for response 2


#class sync_rpc connect to server and allows server to do operations for sync_Rpc
class SYNC_RPC:
    def __init__(self, function, args):
        # intializing variables as in constructor 
        self.function = function
        self.args = args
        self.rpc_type = SYNC
        self.computation_id = None
        self.result = None
        self.req_type = None

    def serverconnect(self,req_type):
        #connects to server for computation adn getting result

        if req_type == 1:
            request = {"function":self.function,"args":self.args,"rpc_type":self.rpc_type,"request_type":SYN}
        
        if req_type == 2:
            request = {"token":self.computation_id,"rpc_type":self.rpc_type,"request_type":REQ}
        
        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect(address)
        sock.send(json.dumps(request).encode())
        response = json.loads(sock.recv(65536).decode())
        sock.close()

        if "error" in response:
            raise RuntimeError(response["error"])
        if "response_type" not in response:
            raise RuntimeError("No response type received from server")

        if req_type == 1:
            self.computation_id = response["token"]
        if req_type == 2:
            self.result = response["result"]
            return self.result



#class async_rpc connect to server and allows server to do operations for async_Rpc

class ASYNC_RPC:
    def __init__(self, function, args):
        # intializing variables as in constructor 
        self.function = function
        self.args = args
        self.rpc_type = ASYNC
        self.computation_id = None
        self.result = None
        self.req_type = None

    def serverconnect(self,req_type):
        #connects to server for computation adn getting result

        if req_type == 1:
            request = {"function":self.function,"args":self.args,"rpc_type":self.rpc_type,"request_type":SYN}
        
        if req_type == 2:
            request = {"token":self.computation_id,"rpc_type":self.rpc_type,"request_type":REQ}
               
        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect(address)
        sock.send(json.dumps(request).encode())
        response = json.loads(sock.recv(65536).decode())
        sock.close()


        if "error" in response:
            raise RuntimeError(response["error"])
        if "response_type" not in response:
            raise RuntimeError("No response type received from server")

        if req_type == 1:
            self.computation_id = response["token"]
            return self.computation_id
        if req_type == 2:
            self.result = response["result"]
            return self.result
        

parser = argparse.ArgumentParser()
parser.add_argument("-rpc")
parser.add_argument("-add")
parser.add_argument("-sort")
args = parser.parse_args()

def sync_procedure(add_args, sort_args):
    add_function = SYNC_RPC("add", args=add_args)
    add_function.serverconnect(1)

    sort_rpc = SYNC_RPC("sort", args=[sort_args])
    sort_rpc.serverconnect(1)

    print("print result for SYNC_RPC")
    print("add", *add_args, " = {}".format(add_function.serverconnect(2)))
    print("sort",*sort_args ," = {}".format(sort_rpc.serverconnect(2)))

def async_procedure(add_args, sort_args):
    add_function = ASYNC_RPC("add", args=add_args)
    print("add function ACK_ID","= {}".format(add_function.serverconnect(1)))

    sort_function = ASYNC_RPC("sort", args=[sort_args])
    print("Sort function ACK_ID","= {}".format(sort_function.serverconnect(1)))
     
    sleep(1)

    print(f"Ack sent from server {host}:{port}")
    
    sleep(2)
    
    print("Async_Rpc is trying to print 10 numbers as a second operation")
    print(*range(1,11))
    
    sleep(2)
     
    print("print result for ASYNC_RPC")
    print("add", *add_args, " = {}".format(add_function.serverconnect(2)))
    print("sort",*sort_args ," = {}".format(sort_function.serverconnect(2)))



if __name__ == "__main__":

    # hence we parsered arguements we are eval them by each 
    rpc_type = args.rpc
    add_args = eval(args.add)
    sort_args = eval(args.sort)

    #Based on rpc type we will let code tocomputen print result
    if rpc_type == "sync":
        sync_procedure(add_args, sort_args)
    elif rpc_type == "async":
        async_procedure(add_args, sort_args)
    else:
        print("Please select RPC type from synv and async")
        exit(1)
