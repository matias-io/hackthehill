# Commands

# upload:filename:number:`chunk`

# Return list of all files in system seperated by comas
# ls

# Return list of all chunk files seperated by comas
# cls

# Download all available chunks of a file
# download:filename

import sys
import socket
import selectors
import types
import chunks

USERS = [
    {
        'ip': '127.0.0.1',
        'port': 12342,
        'name': 'Antoine'
    },
    {
        'ip': '127.0.0.1',
        'port': 12399,
        'name': 'Lucas'
    }
]

def findUser(name):
    for u in USERS:
        if u['name'].lower() == name.lower():
            return u
    print('Could not find user')
    exit()

user = findUser(sys.argv[1])
PORT = user['port']
username = user['name']

rootPath = '/Users/antoine/Documents/PP/hackthehill/asocket/server/' + username

chunksServer = chunks.Chunks(rootPath + '/chunks', rootPath + '/clean')

sel = selectors.DefaultSelector()

lsock = socket.socket()
lsock.bind(('', PORT))
lsock.listen()
print(f"Listening on {PORT}")
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)

def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read
    print(f"Accepted connection from {addr}")
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)

def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Should be ready to read
        if recv_data:
            data.outb += recv_data
        else:
            print(f"Closing connection to {data.addr}")
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            if data.outb == 'c'.encode():
                print("Closing socket")
                sock.close()
                exit()

            dataString = str(data.outb.decode())

            if dataString.startswith('upload'):
                parts = data.outb.decode().split(':')
                print('Uploading')
                filename = parts[1]
                number = parts[2]
                data.outb = parts[3]
                chunksServer.writeChunkFile(filename, number, data.outb.encode())
                sock.send("Ok".encode())
            
            elif dataString.startswith('ls'):
                l = chunksServer.listFiles()
                mes = ''
                for i in l:
                    mes = mes + i + ':'
                
                sock.send(mes[:-1].encode())
            
            elif dataString.startswith('cls'):
                l = chunksServer.listChunkFiles()
                mes = ''
                for i in l:
                    mes = mes + i + ':'

                if mes == '':
                    mes = 'No files'
                
                sock.send(mes[:-1].encode())

            elif dataString.startswith('download'):
                parts = data.outb.decode().split(':')
                print('Downloading')
                filename = parts[1]
                to_send = chunksServer.readAllChunks(filename)

                for i, s in to_send.items():
                    print('Sending chunk ' + str(i))
                    mes = str(i) + ':' + str(len(s)) + ':' + s.decode()
                    sock.send(mes.encode())
                
                sock.send("Ok".encode())

            else:
                print('Invalid command: ', dataString)
                sock.send('Invalid command'.encode())

            data.outb = ''.encode()

try:
    while True:
        events = sel.select(timeout=None)
        for key, mask in events:
            if key.data is None:
                accept_wrapper(key.fileobj)
            else:
                service_connection(key, mask)
except KeyboardInterrupt:
    print("Caught keyboard interrupt, exiting")
finally:
    sel.close()