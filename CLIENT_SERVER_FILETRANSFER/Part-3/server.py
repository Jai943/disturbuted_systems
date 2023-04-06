
import json,random
from socket import socket, AF_INET, SOCK_STREAM

host, port = '127.0.0.1',8054
address = (host, port)
 
def log_response_json(conn, msg):
    res = json.dumps({"error": msg})
    conn.send(res.encode())

TABLE = {}

def add(i, j): #compute - add
    return i + j

def sort(nums): #compute - sort
    return sorted(nums)


SYNC = 0  #rpc code for sync is 0
ASYNC = 1  #rpc code for sync is 1

SYN = ACK = 1  #code for request 1
REQ = 2  #code for response 2


def RPC(connect, address, request_inplace):
    request_id = json.loads(request_inplace)
    if "rpc_type" not in request_id:
        log_response_json(connect, "rpc type missing")

    if request_id["rpc_type"] == SYNC:
        if request_id.get("function"):
            print(f"Client {address[0]}:{address[1]}")
            print(f'Synchronous RPC {request_id.get("function")}')
        YNC_RPC(connect, request_id)
    elif request_id["rpc_type"] == ASYNC:
        if request_id.get("function"):
            print(f"Client {address[0]}:{address[1]}")
            print(f"Ack was sent to client {address[0]}:{address[1]} from server {host}:{port}")
            print(f'Asynchronous RPC {request_id.get("function")}')   
        YNC_RPC(connect, request_id)
 
def YNC_RPC(connect, request_id):
    if request_id["request_type"] in [SYN, ASYNC]:
        token = random.randint(1, 10000)
        funct_ion = globals().get(request_id["function"])
        if not funct_ion:
            log_response_json(connect, "called no function")
            return
        reply = json.dumps({"response_type": ACK, "token": token})
        connect.send(reply.encode())
        try:
            result = funct_ion(*request_id["args"])
            TABLE[token] = result
        except Exception:
            log_response_json(connect, "Error")
    elif request_id["request_type"] == REQ:
        token = int(request_id["token"])
        result = TABLE[token]
        reply = json.dumps({"result": result, "response_type": REQ})
        connect.send(reply.encode())
    else:
        log_response_json(connect, "Invalid type of request")


if __name__ == "__main__":
    with socket(AF_INET, SOCK_STREAM) as sock:
        sock.bind(address)
        sock.listen(10)
        print(f"connection open at : {address[0]}:{address[1]}")
        while True:
            conn, addr = sock.accept()
            req = conn.recv(65536).decode()
            RPC(conn, addr, req)
            conn.close()
