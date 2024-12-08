"""EX 2.6 protocol implementation
   Author: Daniel Reiman
   Date:
"""
from socket import socket

LENGTH_FIELD_SIZE = 2
PORT = 8820

def check_cmd(data: str):
    commands = ["TAKE_SCREENSHOT", "SEND_FILE", "DIR", "DELETE", "COPY", "EXECUTE"]
    if data.upper() in commands:
        return True
    return False

def create_msg(data):
    # Convert the length to 2 digits number
    length = str(len(data)).zfill(LENGTH_FIELD_SIZE)
    message = length + data
    print(message)
    return message

def get_msg(my_socket: socket):
    length = my_socket.recv(LENGTH_FIELD_SIZE).decode()

    if length.isnumeric() is not True:
        return False, "Response length is not numeric or defined properly"
    message = my_socket.recv(int(length)).decode()
    return True, message
