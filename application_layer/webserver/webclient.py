# RRotundu 2024
# A simple web client that makes TCP connection to webserver
# Does GET, POST, PUT and DELETE tests on webserver.py
import sys
import socket

# Global variables
VERSION = "HTTP/1.1"

def reply_parse(reply):
    code = ""
    data = ""

    if(reply.split()[1] != "200"):
        code = reply.split("\n")[0]
        print(reply.split()[1])
        return code, data
    else:
        code = reply.split("\n")[0]
        data = reply.split("\n\n")[-1]
        return code, data

    return 0

# Build the actual request header
def request_build(req_type, file_name):
    req = req_type + " " + '/' + file_name + " " + VERSION + "/n/n"
    return req

def request_send(req_type, file_name, client_socket):
    match req_type:
        case "GET":
            print(req_type + "-ing" + " " + file_name)

            req = request_build("GET", file_name)
            client_socket.send(req.encode())
            code, data = reply_parse(client_socket.recv(1024).decode())
            print("REPLY: " + code)
            if(data != ""):
                f = open("received.html", "w")
                f.write(data)
                f.close()
                return 1
        case "POST":
            print(req_type + "-ing" + " " + file_name)
            req = request_build("POST", file_name)
            f = open(file_name, "r")
            req =  req + f.read()
            client_socket.send(req.encode())
            code, data = reply_parse(client_socket.recv(1024).decode())
            print("REPLY: " + code)
            f.close()
            return 0
        case "PUT":
            return 0
        case "DELETE":
            print(req_type + "-ing" + " " + file_name)
            req = request_build("DELETE", file_name)
            client_socket.send(req.encode())
            code, data = reply_parse(client_socket.recv(1024).decode())
            print("REPLY: " + code)
            return 0

# Start the webclient
def webclient_start(server_address="127.0.0.1", server_port=80, mode=0):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_address, int(server_port)))
    match int(mode):
        # GET send_test.html, save as received.html
        case 0:
            print("Sending GET")
            request_send("GET", "send_test.html", client_socket)
            return 0
        # POST send_test.html, save as posted.html
        case 1:
            print("Sending POST")
            request_send("POST", "send_test.html", client_socket)
            return 0
        # PUT
        case 2:
            print("Sending PUT")
            request_send()
            return 0
        # DELETE
        case 3:
            print("Sending DELETE")
            request_send("DELETE", "deletethis.html", client_socket)
            return 0

    print(f"No match to {mode}")
    return 0

if __name__ == "__main__":
    if(len(sys.argv) == 4):
        address = sys.argv[1]
        port = sys.argv[2]
        mode = sys.argv[3]

        print(f"Using {address} and {port} as client specs, mode {mode}")
        webclient_start(address, port, mode)
    else:
        print("Using default LOCALHOST and PORT=5500 as client specs, in mode 0(GET)")
        webclient_start()