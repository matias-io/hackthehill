# Commands 

# upload:filename:number:`chunk`

import socket
import chunks

chunks = chunks.Chunks('/Users/antoine/Documents/PP/hackthehill/asocket/server/chunks', '/Users/antoine/Documents/PP/hackthehill/asocket/server/clean')

# Create socket
s = socket.socket()
print("Created socket")

port = 12349

s.bind(('127.0.0.1', port))
print("Socket binded to port", port)

s.listen()
c, addr = s.accept()

with c:
    print(f"Connected by {addr}")

    while True:

        data = c.recv(1024)

        if data == 'c'.encode():
            print("Closing socket")
            s.close()
            exit()

        parts = data.decode().split(':')
        print(parts[0])

        if parts[0] == 'upload':
            filename = parts[1]
            number = parts[2]
            data = parts[3]
            chunks.writeChunkFile(filename, number, data.encode())

        print(data)
        c.sendall("Ok".encode())

