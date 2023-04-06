from pathlib import Path
from sys import argv, exit, stderr
from select import select as sel
from socket import socket, AF_INET, SOCK_STREAM


ip="127.0.0.1"
port=8972
if not (len(argv) >= 3):
    print("ERROR:", "Insufficient arguments provided, please try again!", file=stderr)
    exit(True)

call = argv[1].lower()
soc_address = (ip, port)
buffer_size = 68726

def fileop(button):
    match button.split():
        case ['upload']:
            file = Path(fname)
            if not file.is_file():
                print("ERROR:", f"file name invalid, please provide correct file name{fname}!", file=stderr)
                exit(True)

            data = "{}\n{}\n{}".format("upload", file.name, file.read_text()).encode()
            socket.sendto(data, soc_address)

        case ['download']:
            socket.send("{}\n{}".format("download", fname).encode())
            if not sel([socket], [], [], 1)[0]:
                print("ERROR:", f"data Download timeout, please try again {fname}!", file=stderr)
                exit(True)

            file_content, _ = socket.recvfrom(buffer_size)
            Path("client_data/").mkdir(parents=True, exist_ok=True)
            Path("client_data/{}".format(fname)).write_text(file_content.decode())

        case ['delete']:
            data = "{}\n{}".format("delete", fname).encode()
            socket.sendto(data, soc_address)

        case ['rename']:
            new_fname = argv[3]
            data = "{}\n{}\n{}".format("rename", fname, new_fname).encode()
            socket.sendto(data, soc_address)

if __name__ == "__main__":
    with socket(AF_INET, SOCK_STREAM) as socket:
            socket.connect(soc_address)
            fname = argv[2]
            if call == "upload":
                button = 'upload'
                fileop(button)
            elif call == "download":
                button = 'download'
                fileop(button)
            elif call == "delete":
                button = 'delete'
                fileop(button)
            elif call == "rename":
                button = 'rename'
                fileop(button)
            else:
                print("ERROR:", "Operation not found!, try again", file=stderr)
                exit(True)
