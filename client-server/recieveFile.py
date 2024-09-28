import socket

def receive_file():
    s = socket.socket()
    s.connect(('127.0.0.1', 7001))  
    with open('received', 'wb') as file:
        data = s.recv(1024)  # Receive data in small chunks (1024 bytes)
        while data:
            file.write(data)
            data = s.recv(1024)

    print("File received!")
    s.close()

if __name__ == "__main__":
    receive_file()