# Commands

# Quitting
# c

# Sending a chunk file
# sc:filename:number

import chunks
import socket

chunks = chunks.Chunks('/Users/antoine/Documents/PP/hackthehill/asocket/client/chunks', '/Users/antoine/Documents/PP/hackthehill/asocket/client/clean')

s = socket.socket()

port = 12349

s.connect(('127.0.0.1', port))
print("Connected")

while True:
    new = input('>')

    if new == 'c':
        s.sendall(new.encode())
        s.close()
        print("Closing socket")
        exit()

    if new.startswith('sc'):
        splits = new.split(':')
        filename = splits[1]
        number= splits[2]

        c = chunks.readChunkFile(filename, number)

        mes = 'upload:' + filename + ":" + number + ":" + c.decode()
        print(mes)
    
    s.sendall(mes.encode())
    data = s.recv(1024)
    print(data.decode())

s.close()

