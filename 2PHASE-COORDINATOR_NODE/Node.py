
import logging
import socket

HOST = '127.0.0.1' 
PORT = 1224      


def send(conn, msg):
    #to send msg to host 
    print('Send', msg)
    conn.sendall(msg.encode())

def receive(conn):
    #to receive data from host
    data = conn.recv(1024).decode()
    print('Receive', data)
    return data

def ask_input(msg, yes, nope):
    # Ask for an input. like vote yes or no (commit or abort)
    while True:
        answer = input(f'{msg} ({yes}/{nope}) ')
        if answer == yes:
            return True
        if answer == nope:
            return False


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    
    logging.basicConfig(level=logging.INFO,format="%(asctime)s - %(name)s - [ %(message)s ]",datefmt='%d-%b-%y %H:%M:%S',
    force=True,handlers=[logging.FileHandler("node_out.log"),logging.StreamHandler() ])

    while True:
        try:
            data = receive(s)

            if data.startswith('Prepare Sending :- '):
                request = data.split(' ', 1)[1]
                print('Start')

                if ask_input('Ready to commit type yes else type no?', 'yes', 'no'):
                    logging.info('ready')
                    send(s, 'VOTE-COMMIT')
                else:
                    logging.info('abort')
                    send(s, 'VOTE-ABORT')

            print('READY')
            data = receive(s)

            if data == 'GLOBAL-ABORT':
                logging.info('abort')
                print('ABORT')
            elif data == 'GLOBAL-COMMIT':
                logging.info('commit')
                print('COMMIT', request)
            send(s, 'ACK')
        except KeyboardInterrupt:
            print('ending connection')
            break
