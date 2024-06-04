# A basic mail client
import socket
import sys
import ssl

# Test
import base64

# Message components
DOMAIN = 'smtp.gmail.com'
ORIGIN = "raz@testmail.com"
DEST = ""
MSG ="Subject: Test Message\r\nHello this is a test message"
ENDMSG = "\r\n.\r\n"

# Target mail server
SERVER = ""
PORT = ""

# Client Socket
CLIENT_SOCKET = ""

# AUTH stuff
USER = "user"
PASS = "pass"
# SMTP Commands and expected reply codes
R_CODES = {"HELO" :"250",
"EHLO" :"250",
"MAIL FROM" :"250",
"RCPT TO": "250",
"DATA" :"354",
"QUIT" :"221",
"AUTH LOGIN" :"334"}

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
    # CLIENT_SOCKET.send(data_content.encode())
    CLIENT_SOCKET.sendall(data_content)

# Receive and decode a message from the open TCP connection
def get_data():
    data = CLIENT_SOCKET.recv(1024).decode()
    return data

# Send a SMTP command to the open connection
def send_command(type, data=""):
    # match type:
    #     case "HELO":
    #         msg = f"{type} {data}"
    #     case _:
    #         msg = f"{type}: <{data}>"
    msg = f"{type} {data}" if(type == "HELO" or type == "AUTH LOGIN") else f"{type}: <{data}>"
    msg = msg + "\r\n"
    code = R_CODES[type]
    send_data(msg.encode())
    print(f"Client: {msg}")
    m = get_data()
    print(f"Server: {m}")
    if(m[:3] != code):
        print(error_msg(code))
        raise Exception(f"{type} error")

# sends email content
def send_content(content, mode):
    code = ""
    match mode:
        # Content is a username
        case "user":
            code = "334"
            c = content + "\r\n"
            print(f"Content: {c}")
            c = base64.b64encode(c.encode())
            print(f"Content encoded to: {c}")
        # Content is a password
        case "pass":
            code = "235"
            c = content
            print(f"Content: {c}")
            c = base64.b64encode(c.encode())
            print(f"Content encoded to: {c}")
        #Content is mail text
        case "body":
            c = content + ENDMSG
            c = c.encode()
            code = "250"
    send_data(c)
    m = CLIENT_SOCKET.recv(1024).decode()
    print(f"Server: {m}")
    if(m[:3] != code):
        raise Exception(error_msg(code))

# Send an email to the open connection
def send_mail(mail_text):
    try:
        send_command("HELO", DOMAIN)

        send_command("AUTH LOGIN")

        send_content(USER, "user")
        send_content(PASS, "pass")

        send_command("MAIL FROM", ORIGIN)
        send_command("RCPT TO", DEST)
        send_command("DATA")
        
        send_content(mail_text, "body")

        send_command("QUIT")
        return 0
    except Exception as e:
        print(f"Unable to send message({e})")
        return -1

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
    print(f"Server: {m}")
    if m[:3] != "220":
        print(error_msg("220"))
        raise Exception("Invalid server address")
    else:
        return client_socket
if __name__ == "__main__":
    if(len(sys.argv) != 2):
        print("Usage: smtp_client MailAddress:MailPort:DestinationAddr")
    else:
        target = sys.argv[1].split(":")
        if(len(target) != 3):
            print("Usage: smtp_client MailAddress:MailPort:DestinationAddr")
        else:
            ADDRESS = target[0]
            PORT = target[1]
            DEST = target[2]
            print(f"Address: {ADDRESS}\nPort: {PORT}\nDestination: {DEST}")
            try:
                CLIENT_SOCKET = connect_mailServer(ADDRESS, PORT)
                send_mail(MSG)
                CLIENT_SOCKET.close()
                # print("Message sent")
            except Exception as e:
                print(f"Failed to connect to server: {e}")