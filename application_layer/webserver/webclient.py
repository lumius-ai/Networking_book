# RRotundu 2024
# A simple web client that makes TCP connection to server and does GET, POST, PUT and DELETE
import sys
import socket

# Start the webclient
def webclient_start(server_address="127.0.0.1", server_port=5500):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_address, server_port))
    
    return 0

if __name__ == "__main__":
    if(len(sys.argv) == 3):
        address = sys.argv[1]
        port = sys.argv[2]
        print(f"Using {address} and {port} as client specs")
    print("Using LOCALHOST and PORT=5500 as client specs")
    webclient_start()