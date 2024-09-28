import socket

def send_file():
    s = socket.socket()
    s.bind(('0.0.0.0', 5001)) # using port 5001
    s.listen(1)
    print("...Waiting for a connection...")

    conn, addr = s.accept()
    print(f"Connected by {addr}")

    with open('example.txt', 'rb') as file:  
        conn.sendfile(file)  

    print("File sent!")
    conn.close()

if __name__ == "__main__":
    send_file()
