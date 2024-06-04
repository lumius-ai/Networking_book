import socket
import ssl
import sys

ACTIVE_SOCKET = ""
ADDRESS = 'smtp.gmail.com'
PORT = '587'

def error_msg(error_code):
    print(f"{error_code} not received, aborting")

# TCP connect to a server, return an ssl wrapped socket
def connect_server(addr, port):
    cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cs.settimeout(10)
    cs.connect((addr, int(port)))
    #SSL wrap socket
    ws = wrap_socket(cs)
    return ws

# TCP connect to an SMTP mail server
def connect_mailServer(s_addr, s_port):
    client_socket = connect_server(s_addr, s_port)
    m = client_socket.recv(1024).decode()
    print(m)
    if m[:3] != "220":
        print(error_msg("220"))
        raise Exception("Invalid server address")
    else:
        return client_socket

def wrap_socket(sock):
    # Create a default SSL context
    context = ssl.create_default_context()
    # Wrap the socket with SSL
    ssl_sock = context.wrap_socket(sock, server_hostname=ADDRESS)
    return ssl_sock

if __name__ == "__main__":
    address = 'smtp.gmail.com'
    port = '465'
    ACTIVE_SOCKET = connect_mailServer(address, port)
    ACTIVE_SOCKET.close()

