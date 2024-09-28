# Commands

# Quitting
# c

# Sending a chunk file (file in client/chunks)
# sc:filename:number

# Sending a full file (file in client/clean)
#sf:filename

# Reconstruct file from chunks (server side)
#r:filename

import chunks
import socket

chunksClient = chunks.Chunks('/Users/antoine/Documents/PP/hackthehill/asocket/client/chunks', '/Users/antoine/Documents/PP/hackthehill/asocket/client/clean')
chunksServer = chunks.Chunks('/Users/antoine/Documents/PP/hackthehill/asocket/server/chunks', '/Users/antoine/Documents/PP/hackthehill/asocket/server/clean')

s = socket.socket()

port = 12345

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

        c = chunksClient.readChunkFile(filename, number)

        mes = 'upload:' + filename + ":" + number + ":" + c.decode()
        print(mes)
        
        s.sendall(mes.encode())
        data = s.recv(1024)
        print(data.decode())

    if new.startswith('sf'):
        splits = new.split(':')
        filename = splits[1]

        c = chunksClient.deconstructFile(filename)
        index = 1

        for chunk in c:
            print("Sending chunk", str(index))
            mes = 'upload:' + filename + ":" + str(index) + ":" + chunk.decode()
            s.sendall(mes.encode())
            data = s.recv(1024)
            print(data.decode())
            index = index + 1

    if new.startswith('r'):
        splits = new.split(':')
        filename = splits[1]

        d = chunksServer.readFullFile(filename)
        chunksServer.writeFullFile(filename, d)


