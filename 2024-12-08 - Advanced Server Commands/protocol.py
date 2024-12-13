
from socket import socket

LENGTH_FIELD_SIZE = 7
PORT = 8820

def check_cmd(data: str):
    commands = ["TAKE_SCREENSHOT", "SEND_FILE", "DIR", "DELETE", "COPY", "EXECUTE"]
    return data.upper() in commands

def create_msg(data):
    # Convert the length to 2 digits number
    length = str(len(data)).zfill(LENGTH_FIELD_SIZE)
    message = length + data
    return message

def get_msg(my_socket: socket):
    length = my_socket.recv(LENGTH_FIELD_SIZE).decode()
    if length.isnumeric() is not True:
        return False, f"Response length is not numeric or defined properly"
    message = my_socket.recv(int(length)).decode()
    return True, message
