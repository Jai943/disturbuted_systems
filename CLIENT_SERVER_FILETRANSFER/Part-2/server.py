import os,socket
from pyftpdlib.servers import FTPServer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.authorizers import DummyAuthorizer

sync_sdir = 'server-data/server-sync'
sync_sfldr = os.path.join(os.getcwd(), sync_sdir)
sync_sfile = '.pyftpsync-meta.json'

if os.path.exists('server-data/server-sync/.pyftpsync-meta.json'):
    os.remove(os.path.join(sync_sfldr, sync_sfile))
else:
    pass

address = (socket.gethostbyname(socket.gethostname()),2763)

def RPC_CONN():
    authorizer = DummyAuthorizer()
    authorizer.add_anonymous(os.getcwd(), perm='elradfmwMT')
    
    handler = FTPHandler
    handler.authorizer = authorizer
    handler.permit_foreign_addresses = True

    server = FTPServer(address, handler)
    server.serve_forever()

if __name__ == '__main__':
    RPC_CONN()
