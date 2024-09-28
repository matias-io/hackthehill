import chunks
import socket

# Commands

# Sending a chunk file (file in client/chunks)
# sc:filename:number

# Sending a full file (file in client/clean)
# sf:filename

# Reconstruct file from chunks (server side)
# r:filename

# List all available files in network
# ls

# Downloading file
# d:filename

### User Directory ###
USERS = [
    {
        'ip': '127.0.0.1',
        'port': 12342,
        'name': 'Antoine'
    },
    {
        'ip': '127.0.0.1',
        'port': 12399,
        'name': 'Aditya'
    }
]

i = 0
for user in USERS:
    try:
        s = socket.socket()
        s.connect((user['ip'], user['port']))
        user['socket'] = s
        print("Connected to " + user['name'])
    except:
        print("User " + user['name'] + ' is not available')
        del USERS[i]
        continue

    i = i + 1

# List of all files in the network
all_files = []

chunksClient = chunks.Chunks('/Users/antoine/Documents/PP/hackthehill/asocket/client/chunks', '/Users/antoine/Documents/PP/hackthehill/asocket/client/clean')
chunksServer = chunks.Chunks('/Users/antoine/Documents/PP/hackthehill/asocket/server/chunks', '/Users/antoine/Documents/PP/hackthehill/asocket/server/clean')

while True:
    new = input('> ')

    if new.startswith('sc'):
        splits = new.split(':')
        filename = splits[1]
        number= splits[2]

        c = chunksClient.readChunkFile(filename, number)

        mes = 'upload:' + filename + ":" + number + ":" + c.decode()
        print(mes)
        
        USERS[0]['socket'].sendall(mes.encode())
        data = USERS[0]['socket'].recv(1024)
        print(data.decode())

    if new.startswith('sf'):
        USERS[0]['socket'].connect((USERS[0]['ip'], USERS[0]['port']))
        print("Connected to " + USERS[0]['name'])
        splits = new.split(':')
        filename = splits[1]

        c = chunksClient.deconstructFile(filename)
        index = 0

        for chunk in c:
            print("Sending chunk", str(index))
            mes = 'upload:' + filename + ":" + str(index) + ":" + chunk.decode()
            USERS[0]['socket'].sendall(mes.encode())
            data = USERS[0]['socket'].recv(1024)
            print(data.decode())
            index = index + 1

    if new.startswith('ls'):
        for user in USERS:
            user['socket'].sendall('ls'.encode())
            data = user['socket'].recv(1024)
            files = data.decode().split(':')
            all_files.extend(files)

            all_files = list(dict.fromkeys(all_files))

            print(all_files)

    if new.startswith('r'):
        splits = new.split(':')
        filename = splits[1]

        d = chunksServer.readFullFile(filename)
        chunksServer.writeFullFile(filename, d)

    if new.startswith('d'):
        splits = new.split(':')
        filename = splits[1]

        USERS[0]['socket'].sendall(('download:' + filename).encode())

        all_chunks = {}

        while True:
            data = USERS[0]['socket'].recv(1024)
            print('Received ' + data.decode())
            print('Over')

            #format is number:chunk

            while len(data) != 0:

                if data.decode() == 'Ok':
                    break

                parts = data.decode().split(':')
                number = int(parts[0])
                start = str(number) + ':' + parts[1]
                buffer_size = int(parts[1]) + len(start.encode())
                temp_data = data[0: buffer_size + 1]
                print('Temp data: ' + str(temp_data))
                print('Left', len(data))
                data = data[buffer_size+1:]
                print(data)

                temp_parts = temp_data.decode().split(':')
                buffer = temp_parts[2]

                all_chunks[number] = buffer
            
            if data.decode() == 'Ok':
                break

        print(all_chunks)

        # Order all the buffers
        chunks_ordered = []
        i = 0

        while i < len(all_chunks):
            chunks_ordered.append(all_chunks[i].encode())
            i = i + 1
        
        
        chunksClient.reconstrucFile(filename, chunks_ordered)




