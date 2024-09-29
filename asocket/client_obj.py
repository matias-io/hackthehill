import chunks
import socket
from users import UserTable, findUser, LOCAL_IP, LOCAL_NAME, LOCAL_PORT
import os

class Client:

    # List of all files in the network
    all_files = []
    all_users = UserTable()
    users = all_users.users.copy()
    root_path = '/Users/antoine/Documents/PP/hackthehill/asocket'
    chunksClient = chunks.Chunks(root_path + '/client/chunks', root_path + '/client/clean')
    
    def __init__(self, root_path='/Users/antoine/Documents/PP/hackthehill/asocket') -> None:
        self.root_path = root_path
        self.chunksClient = chunks.Chunks(root_path + '/client/chunks', root_path + '/client/clean')

        self.connect_to_hosts()

        # Make sure that the paths exists
        try:
            os.makedirs(self.root_path + '/client')
            os.makedirs(self.root_path + '/client/chunks')
            os.makedirs(self.root_path + '/client/clean')
        except:
            return

    # Attempts to reconnect to all hosts in the network
    def connect_to_hosts(self):
        i = 0
        self.users = self.all_users.users.copy()
        while i < len(self.users):
            try:
                s = socket.socket()
                s.connect((self.users[i]['ip'], self.users[i]['port']))
                self.users[i]['socket'] = s
                print("Connected to " + self.users[i]['name'])
                i = i + 1
            except:
                print("User " + self.users[i]['name'] + ' is not available')
                del self.users[i]
                continue

        if len(self.users) == 0:
            print("No one is connected to network")

    # Update the user table by asking all hosts
    def user_table_update(self):
        data = ''.encode()

        for user in self.users:
            user['socket'].sendall((f'users:{LOCAL_NAME}:{LOCAL_IP}:{LOCAL_PORT}').encode())

            while True:
                temp = user['socket'].recv(1024)
                if temp.decode().endswith('}'):
                    data = data + temp[:-1]
                    break
                else:
                    data = data + temp
            
        user_strings = data.split('|')

        for user_s in user_strings:
            s = user_s.split(':')
            name = s[0]
            ip = s[1]
            port = s[2]
            if self.all_users.checkUser(name) == False:
                self.add_user(name, ip, port)

    
    # Updates the path where files are taken and where files are put to
    def update_path(self, new):
        self.chunksClient.setPath(new)

    # Upload a specific chunk to a specific host
    def upload_chunk_to_host(self, filename, number, hostdest):
        user = findUser(self.users, hostdest)

        c = self.chunksClient.readChunkFile(filename, number)

        mes = 'upload:' + filename + ":" + number + ":" + c.decode()
        print(mes)
        
        user['socket'].sendall(mes.encode())
        data = user['socket'].recv(1024)
        print(data.decode())

    # Upload a file to a specific host
    def upload_file_to_host(self, filename, hostdest):
        user = findUser(self.users, hostdest)


        c = self.chunksClient.deconstructFile(filename)
        index = 0

        for chunk in c:
            print("Sending chunk", str(index))
            mes = 'upload:' + filename + ":" + str(index) + ":" + chunk.decode()
            user['socket'].sendall(mes.encode())
            data = user['socket'].recv(1024)
            print(data.decode())
            index = index + 1

    # Upload file in a distributed way to the system
    def upload_file_distributed(self, filename):
        c = self.chunksClient.deconstructFile(filename)
        userNum = 0

        for user in self.users:
            index = userNum
            while index < len(c):
                print("Sending chunk", str(index))
                mes = 'upload:' + filename + ":" + str(index) + ":" + c[index].decode()
                user['socket'].sendall(mes.encode())
                data = user['socket'].recv(1024)
                print(data.decode())
                index = index + len(self.users)
            userNum = userNum + 1

    # List all available files in the system
    def ls(self):
        for user in self.users:
            user['socket'].sendall('ls'.encode())
            data = user['socket'].recv(1024)
            files = data.decode().split(':')
            self.all_files.extend(files)

            self.all_files = list(dict.fromkeys(self.all_files))
            for f in self.all_files:
                print(f)
        
        return self.all_files

    # List all the chunks of a host
    def chunk_list(self, hostdest):
        user = findUser(self.users, hostdest)
        user['socket'].sendall('cls'.encode())
        data = user['socket'].recv(1024)
        files = sorted(data.decode().split(':'))
        for f in files:
            print(f)

        return files

    # Delete file for all hosts
    def delete_file(self, filename):
        for user in self.users:
            msg = 'delete:' + filename
            user['socket'].sendall(msg.encode())
            data = user['socket'].recv(1024)
            print(data.decode())

    # Add user
    def add_user(self, name, ip, port):
        self.all_users.addUser(name, ip, port)
        self.connect_to_hosts()

    # Download a file from a specific host
    def download_file_host(self, filename, hostdest):
        user = findUser(self.users, hostdest)


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
        
        
        self.chunksClient.reconstrucFile(filename, chunks_ordered)

    # Download a file from all hosts
    def download_file(self, filename):
        data = ''.encode()
        all_chunks = {}

        for user in self.users:
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
            try:
                chunks_ordered.append(all_chunks[i].encode())
            except:
                print('Chunks are missing for a file. Aborting')
                break
            i = i + 1
        
        
        self.chunksClient.reconstrucFile(filename, chunks_ordered)