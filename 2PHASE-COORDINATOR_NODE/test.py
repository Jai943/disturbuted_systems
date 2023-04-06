import logging
from multiprocessing import Lock
import socket
import threading

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 1224        # Port to listen on (non-privileged ports are > 1023)

class Coordinate:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clients = []
        self.started = False
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listen_thread = threading.Thread(target=self.accept)
        self.counter = 0
        self.countermessage = 'Prepare Sending :- down'
        self.socket.bind((self.host, self.port))
        self.socket.listen()

    def accept(self):
        #Accept connections from clients in a separated thread. and also waits for all the client conns
        #lock = lock()
        
        while self.started:
            #lock.acquire()
            conn, _ = self.socket.accept()
            #self.counter += 1
            #lock.release()
            self.clients.append(conn)
            #if self.counter == '3':
             #   self.stop()


    def start(self):
        # Start the server.
        self.started = True
        self.listen_thread.start()

    def stop(self):
        # Stop the server. (close the connections)
        self.started = False
        for client in self.clients:
            client.close()
        self.listen_thread.join()
        self.socket.close()

    def send(self, msg):
        #Sends a message to all nodes.
        print('Send', msg)
        for client in self.clients:
            #print(msg.encode())
            if msg == self.countermessage:
                #print('condition worked')
                if self.counter == 2:

                    logging.info('abort')
                    self.send('GLOBAL-ABORT')
                    print('ABORT')
                    return

            self.counter += 1   
            #print('second condition worked')
            client.sendall(msg.encode())


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,format="%(asctime)s - %(name)s - [ %(message)s ]",datefmt='%d-%b-%y %H:%M:%S',
    force=True,handlers=[logging.FileHandler("coordinator_out.log"),logging.StreamHandler() ])

    server = Coordinate(HOST, PORT)
    server.start()
    try:
        while True:
            x = input('Enter a any kind of query you want:')
                   # running transaction for voting from all nodes.
            
            print('transaction_started')
            logging.info('begin_commit')
            server.send(f'Prepare Sending :- {x}')
            findaborts = set()
            for i in server.clients:
                vote = i.recv(1024)
                if vote:
                    print('Receive', vote.decode())
                    findaborts.add(vote.decode())
                else:
                    server.clients.remove(i)
            xt = findaborts
            if 'VOTE-ABORT' in xt:
                logging.info('abort')
                print('WAIT')
                server.send('GLOBAL-ABORT')
                print('ABORT')
            else:
                logging.info('commit')
                print('WAIT')
                server.send('GLOBAL-COMMIT')
                print('COMMIT', x)
            freshset = set()
            for i in server.clients:
                vote = i.recv(1024)
                if vote:
                    print('Receive', vote.decode())
                    freshset.add(vote.decode())
                else:
                    server.clients.remove(i)
            print(freshset)
            logging.info('transaction_ended')
    except KeyboardInterrupt:
        server.stop()