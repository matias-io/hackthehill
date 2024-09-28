import sys
import socket
import selectors
import types
import chunks

PORT = 12345

chunksServer = chunks.Chunks('/Users/antoine/Documents/PP/hackthehill/asocket/server/chunks', '/Users/antoine/Documents/PP/hackthehill/asocket/server/clean')

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

            parts = data.outb.decode().split(':')

            if parts[0] == 'upload':
                print('Uploading')
                filename = parts[1]
                number = parts[2]
                data.outb = parts[3]
                chunksServer.writeChunkFile(filename, number, data.outb.encode())

            sock.sendall("Ok".encode())

            data.outb = []

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