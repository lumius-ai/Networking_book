# Server code for udpinger exercise
import random
import socket

def server_start():
    server_Socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_Socket.bind(('', 12000))
    print("Socket bound to port 12000")
    while True:
        print("Awaiting messages...")
        rand = random.randint(0, 10)
        message, address = server_Socket.recvfrom(1024)
        print(f"Message: {message}\nFROM: {address}")
        message = message.decode().upper()
        if rand < 4:
            continue
        else:
            server_Socket.sendto(message.encode(), address)

if __name__ == "__main__":
    print("Starting server")
    server_start()