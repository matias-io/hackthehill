import socket

def receive_file():
    s = socket.socket()
    s.connect(('127.0.0.1', 5001))  # Connect to the server (change IP if needed)

    with open('received.txt', 'wb') as file:  # Save the received file
        data = s.recv(1024)  # Receive data in small chunks (1024 bytes)
        while data:
            file.write(data)
            data = s.recv(1024)

    print("File received!")
    s.close()

if __name__ == "__main__":
    receive_file()