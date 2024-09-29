# Commands

# upload:filename:number:`chunk`

# Return list of all files in system seperated by comas
# ls

# Download all available chunks of a file
# download:filename

# 
# 



import sys
import socket
import selectors
import types
import chunks

PORT = 12399

chunksServer = chunks.Chunks('/Users/adityabaindur/Desktop/HTH_LATEST/hackthehill/asocket/server/chunks', 
                             '/Users/adityabaindur/Desktop/HTH_LATEST/hackthehill/asocket/server/clean', 
                             '/Users/adityabaindur/Desktop/HTH_LATEST/hackthehill/asocket/server/hash')


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
            print(dataString)

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











            elif dataString.startswith('wh'):

                parts = data.outb.decode().split(':')

                print('Uploading w HASH')

                filename = parts[1]
                number = parts[2]
                hash = parts[3]

                chunksServer.writeChunkFile(filename, number, data.outb)
                print("\n\n\n chunked \n\n\n")

                chunksServer.writeHashFile(filename, number,hash )


                sock.send("Ok_hashed".encode())












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