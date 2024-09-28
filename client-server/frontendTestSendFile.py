import socket
import sys
import asyncio
import websockets
import os




def send_file(file_path):
    s = socket.socket()
    s.bind(('127.0.0.1', 7001))
    s.listen(1)
    print("Waiting for a connection...")

    conn, addr = s.accept()
    print(f"Connected by {addr}")

    with open(file_path, 'rb') as file:  
        conn.sendfile(file)  

    print("File sent!")
    conn.close()
    
    
async def main():
    async with websockets.serve(frontend_link, '127.0.0.1', 6001):
        print("WebSocket server started on ws://127.0.0.1:6001")
        await asyncio.Future()

async def frontend_link(websocket, path):
    
    file_path = await websocket.recv()
    print(f"Received file path: {file_path}")

    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        await websocket.send(f"File not found: {file_path}")
        return
    else:
        send_file(file_path)
    # Acknowledge receipt of the file path
    await websocket.send(f"File '{file_path}' exists and can be processed.")
    


if __name__ == "__main__":
    asyncio.run(main())


