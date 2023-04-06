
import sys
from pathlib import Path
from threading import Thread
from socket import socket, AF_INET, SOCK_STREAM
import socket


host="127.0.0.1"
port=8972
address = (host, port)
buffer_size = 68726
con_limit = 1024


def operation(command):
    
    match command.split():
        case ['upload']:
            fname, data = args[1].decode().strip(), args[2].decode()
            Path("server_data/").mkdir(parents=True, exist_ok=True)
            Path("server_data/{}".format(fname)).write_text(data)
            print(f"The data {fname} has been uploaded to the server at host:{c_ip} at port:{c_port}")
        
        case ['download']:
            fname = args[1].decode().strip()
            file = Path("server_data/{}".format(fname))
            if file.is_file():
                conn.send(file.read_bytes())
                print(f"The data {fname} has been downloaded from server:{c_ip} at port:{c_port}")
            else:
                print(f"ERROR: {fname} not found - [{c_ip}:{c_port}]")
        case ['delete']:
            fname = args[1].decode().strip()
            file = Path("server_data/{}".format(fname))
            if file.is_file():
                file.unlink()
                print(f"The file {fname} has been deleted from server:{c_ip} at port:{c_port}")
            else:
                print(f"ERROR: The file {fname} cannot be found at host:{c_ip} and port:{c_port}")
        case ['rename']:
            fname = args[1].decode().strip()
            new_fname = args[2].decode().strip()
            file = Path("server_data/{}".format(fname))
            new_file = Path("server_data/{}".format(new_fname))
            if new_file.exists():
                print(f"ERROR: The given file {new_fname} already exists at server:{c_ip} and port:{c_port}")
                if input("do you want to Overwrite the file? [y/N]").lower() == "y":
                    print(f"Overwriting the file <{new_fname}> with existing <{fname}>")
                    file.rename(new_file)
            elif file.is_file():
                file.rename(new_file)
                print(f"The file {fname} is renamed from server at host:{c_ip} and port:{c_port}")
            else:
                print(f"ERROR: the file {fname} not found in server at host: {c_ip} and port at :{c_port}")
        
        case ['default']:
            print("wrong command")
if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket:
        socket.bind(address)
        socket.listen(con_limit)
        print(f"server running and open at IP {address[0]} and port: {address[1]}") 
    
        while True:    
            conn, [c_ip, c_port] = socket.accept()
            print(f"New client connected to server at IP:{c_ip} and port:{c_port}")

            args = conn.recv(buffer_size).split(b"\n", maxsplit=2)
            opp = args[0].decode().strip().lower()
            if opp == "upload":
                command = 'upload'
                operation(command)
            elif opp == "download":
                command = 'download'
                operation(command)
            elif opp == "delete":
                command = 'delete'
                operation(command)
            elif opp == "rename":
                command = 'rename'
                operation(command)
            else:
                print(f"<{opp}>the given method is not available!")