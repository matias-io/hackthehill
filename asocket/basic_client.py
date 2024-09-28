import chunks
import socket

# Commands

# POINT TO POINT

# Sending a chunk file (file in client/chunks)
# sc:filename:number:dest

# Sending a full file (file in client/clean)
# sf:filename:dest

# Downloading file
# down:filename:source

# Get all chunks
# cls:dst

# ENTIRE NETWORK

# List all available files in network
# ls

# Distributed upload
# Will split the chunks accross hosts
# dup:filename

# Distributed download
# Will find chunks from everywhere
# ddown:filename

# DEPRECIATED
# Reconstruct file from chunks (server side) 
# r:filename


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
        'name': 'Lucas'
    }
]

def findUser(name):
    for u in USERS:
        if u['name'].lower() == name.lower():
            return u
    print('Could not find user')

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

if len(USERS) == 0:
    print("No one is connected to network")
    exit()


# List of all files in the network
all_files = []

chunksClient = chunks.Chunks('/Users/antoine/Documents/PP/hackthehill/asocket/client/chunks', '/Users/antoine/Documents/PP/hackthehill/asocket/client/clean')
chunksServer = chunks.Chunks('/Users/antoine/Documents/PP/hackthehill/asocket/server/chunks', '/Users/antoine/Documents/PP/hackthehill/asocket/server/clean')

while True:
    new = input('> ')

    if new.startswith('sc'):
        splits = new.split(':')
        filename = splits[1]
        number = splits[2]
        dest = splits[3]
        user = findUser(dest)

        c = chunksClient.readChunkFile(filename, number)

        mes = 'upload:' + filename + ":" + number + ":" + c.decode()
        print(mes)
        
        user['socket'].sendall(mes.encode())
        data = user['socket'].recv(1024)
        print(data.decode())

    if new.startswith('sf'):
        splits = new.split(':')
        filename = splits[1]
        dest = splits[2]
        user = findUser(dest)


        c = chunksClient.deconstructFile(filename)
        index = 0

        for chunk in c:
            print("Sending chunk", str(index))
            mes = 'upload:' + filename + ":" + str(index) + ":" + chunk.decode()
            user['socket'].sendall(mes.encode())
            data = user['socket'].recv(1024)
            print(data.decode())
            index = index + 1

    # Distributed upload
    if new.startswith('dup'):
        splits = new.split(':')
        filename = splits[1]
        c = chunksClient.deconstructFile(filename)
        userNum = 0

        for user in USERS:
            index = userNum
            while index < len(c):
                print("Sending chunk", str(index))
                mes = 'upload:' + filename + ":" + str(index) + ":" + c[index].decode()
                user['socket'].sendall(mes.encode())
                data = user['socket'].recv(1024)
                print(data.decode())
                index = index + len(USERS)
            userNum = userNum + 1

    if new.startswith('ls'):
        for user in USERS:
            user['socket'].sendall('ls'.encode())
            data = user['socket'].recv(1024)
            files = data.decode().split(':')
            all_files.extend(files)

            all_files = list(dict.fromkeys(all_files))

    if new.startswith('cls'):
        splits = new.split(':')
        dest = splits[1]
        user = findUser(dest)
        user['socket'].sendall('cls'.encode())
        data = user['socket'].recv(1024)
        files = sorted(data.decode().split(':'))
        for f in files:
            print(f)

    if new.startswith('r'):
        splits = new.split(':')
        filename = splits[1]

        d = chunksServer.readFullFile(filename)
        chunksServer.writeFullFile(filename, d)

    if new.startswith('down'):
        splits = new.split(':')
        filename = splits[1]
        dest = splits[2]
        user = findUser(dest)


        user['socket'].sendall(('download:' + filename).encode())

        all_chunks = {}

        while True:
            data = user['socket'].recv(1024)
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

    if new.startswith('ddown'):
        splits = new.split(':')
        filename = splits[1]
        data = ''.encode()
        all_chunks = {}

        for user in USERS:
            user['socket'].sendall(('download:' + filename).encode())

            while True:
                temp = user['socket'].recv(1024)
                if temp.decode().endswith('Ok'):
                    data = data + temp[:-2]
                    break
                else:
                    data = data + temp
            
            

            #format is number:chunk

            while len(data) != 0:

                if data.decode() == 'Ok':
                    break

                parts = data.decode().split(':')
                number = int(parts[0])
                start = str(number) + ':' + parts[1]
                buffer_size = int(parts[1]) + len(start.encode())
                temp_data = data[0: buffer_size + 1]
                data = data[buffer_size+1:]
                temp_parts = temp_data.decode().split(':')
                buffer = temp_parts[2]

                all_chunks[number] = buffer
                
            if data.decode() == 'Ok':
                break

        print(all_chunks.keys())

        # Order all the buffers
        chunks_ordered = []
        i = 0

        print(len(all_chunks))
        while i < len(all_chunks):
            print('Assembling chunk ' + str(i))
            chunks_ordered.append(all_chunks[i].encode())
            i = i + 1
        
        
        chunksClient.reconstrucFile(filename, chunks_ordered)




