# A basic mail client
from socket import *

# Message components
MSG ="Hello world"
ENDMSG = "\r\n.\r\n"

# Target mail server
SERVER = ""

# Client Socket
CLIENT_SOCKET = ""

# SMTP Commands and expected reply codes
R_CODES = {"HELO" :"220", 
"MAIL FROM" :"250",
"RCPT TO": "250",
"DATA" :"250",
"QUIT" :"221"}

# Print an error message
def error_msg(error_code):
    print(f"{error_code} not received, aborting")

# Send a message through the open TCP connection
def send_data(data_content):
    CLIENT_SOCKET.send(content.encode())

# Receive and decode a message from the open TCP connection
def get_data():
    data = CLIENT_SOCKET.recv().decode()
    return data

# Send a SMTP command to the open connection
def send_command(type):
    msg = type
    code = R_CODES[type]
    send_data(type)
    m = get_data()
    if(m[:3] == code):
        print(error_msg(code))
        raise Exception(f"{type} error")

# Send an email to the open connection
def send_mail(mail_text):
    break

# TCP connect to a server
def connect_server(s_addr, s_port):
    break

# TCP connect to an SMTP mail server
def connect_mailServer(s_addr, s_part):
    break

if __name__ == "__main__":
    return 1