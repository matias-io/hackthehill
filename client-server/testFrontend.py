import socket
import sys
import os

def send_file(file_path):
    s = socket.socket()
    s.connect(('127.0.0.1', 5001))  # Connect to the server

    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    with open(file_path, 'rb') as file:
        data = file.read(1024)
        while data:
            s.send(data)
            data = file.read(1024)

    print(f"File '{file_path}' sent successfully!")
    s.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python client_script.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]  # Get the file path from the command line argument
    send_file(file_path)
