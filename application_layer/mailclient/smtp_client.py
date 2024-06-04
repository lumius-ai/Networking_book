# A basic mail client
import socket
import sys
import ssl

# Message components
ORIGIN = "raz@testmail.com"
DEST = ""
MSG ="Test Message"
ENDMSG = "\r\n.\r\n"

# Target mail server
SERVER = ""

# Client Socket
CLIENT_SOCKET = ""

# SMTP Commands and expected reply codes
R_CODES = {"HELO" :"220", 
"MAIL FROM" :"250",
"RCPT TO": "250",
"DATA" :"354",
"QUIT" :"221"}

# SSL wrap a socket
def wrap_socket(sock):
    # Create a default SSL context
    context = ssl.create_default_context()
    # Wrap the socket with SSL
    ssl_sock = context.wrap_socket(sock, server_hostname=ADDRESS)
    return ssl_sock
# Print an error message
def error_msg(error_code):
    print(f"{error_code} not received, aborting")

# Send a message through the open TCP connection
def send_data(data_content):
    CLIENT_SOCKET.send(content.encode())

# Receive and decode a message from the open TCP connection
def get_data():
    data = CLIENT_SOCKET.recv(1024).decode()
    return data

# Send a SMTP command to the open connection
def send_command(type, data=""):
    match type:
        case "HELO":
            msg = f"{type} {data}"
        case _:
            msg = f"{type}: <{data}>"
    code = R_CODES[type]
    send_data(msg)
    m = get_data()
    if(m[:3] != code):
        print(error_msg(code))
        raise Exception(f"{type} error")
    else:
        print(m)

# Send an email to the open connection
def send_mail(mail_text):
    try:
        send_command("HELO", ORIGIN)
        send_command("MAIL FROM", ORIGIN)
        send_command("RCPT TO", DEST)
        send_command("DATA")

        CLIENT_SOCKET.send_data(mail_text+ENDMSG)
        m = CLIENT_SOCKET.recv(1024).decode()
        if(m[:3] != "354"):
            raise Exception(error_msg("354"))
        send_command("QUIT")
        return 0
    except Exception as e:
        print("Unable to send message({e})")
        return -1
    break

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
if __name__ == "__main__":
    if(len(sys.argv) != 2):
        print("Usage: smtp_client MailAddress:MailPort:DestinationAddr")
        return 1
    else:
        target = argv[1].split(":")
        if(len(target) != 3):
            print("Usage: smtp_client MailAddress:MailPort:DestinationAddr")
        else:
            address = target[0]
            port = target[1]
            DEST = target[2]
            try:
                CLIENT_SOCKET = connect_mailServer(address, port)
                send_mail(MSG)
            except Exception as e:
                print(f"Failed to connect to server: {e}")
            return 1