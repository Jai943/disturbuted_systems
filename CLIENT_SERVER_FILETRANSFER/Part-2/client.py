import os,time
from ftpsync.targets import FsTarget
from ftpsync.ftp_target import FTPTarget
from ftpsync.synchronizers import BiDirSynchronizer
from socket import gethostbyname, gethostname, AF_INET, SOCK_STREAM, socket

host_address, server_port, cli_ser_port = gethostbyname(gethostname()),2763,8847

sync_dir = 'client-data/client-sync'
sync_file = '.pyftpsync-meta.json'
server_sync_path = '/server-data/server-sync'
sync_fldr = os.path.join(os.getcwd(),sync_dir)

addrs = FTPTarget(path=server_sync_path, host=host_address, port=server_port)

if os.path.exists('client-data/client-sync/.pyftpsync-meta.json'):
    os.remove(os.path.join(sync_fldr, sync_file))
else: 
    pass

if __name__ == "__main__":
    with socket(AF_INET, SOCK_STREAM) as client_sock:
        client_sock.bind((host_address, cli_ser_port))
        client_sock.listen()
        print(f"connected to port")

        hasher = {'resolve':'skip','verbose':4}
        SERVER = BiDirSynchronizer(FsTarget(sync_fldr), addrs, hasher)
        while True:
            SERVER.run()
            time.sleep(4)
