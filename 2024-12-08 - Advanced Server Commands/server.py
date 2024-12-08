"""EX 2.6 server implementation
   Author: Daniel Reiman
   Date:
"""
import io
import os
import socket
import protocol
from PIL import ImageGrab
from datetime import datetime
import random
from protocol import check_cmd
from io import BytesIO

def take_screenshot():
    screenshot = ImageGrab.grab()
    buffer = io.BytesIO()
    screenshot.save(buffer, "PNG") # Store the image in the buffer to send it as bytes
    buffer.seek(0)  # Move to the beginning of the image data
    return buffer.read()


def create_server_rsp(cmd: str, parameter: str):
    commands = ["TAKE_SCREENSHOT", "SEND_FILE", "DIR", "DELETE", "COPY", "EXECUTE"]

    match cmd:
        case "TAKE_SCREENSHOT":
            return take_screenshot()
        case "SEND_FILE":
            return "File is being sent"
        case "DIR":
            return "Directory listing"
        case "DELETE":
            return "File is deleted"
        case "COPY":
            return "File is copied"
        case "EXECUTE":
            return "Command executed"
        case _:
            return "Unknown command"


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", protocol.PORT))
    server_socket.listen()
    print("Server is up and running")
    (client_socket, client_address) = server_socket.accept()
    print("Client connected")

    try:
        while True:
            valid_msg, messaage = protocol.get_msg(client_socket)
            (cmd, parameter) = messaage.split(" ")

            if valid_msg:
                print(cmd)
                if check_cmd(cmd):
                    response = protocol.create_msg(create_server_rsp(cmd, parameter))
                else:
                    response = "Wrong command"
            else:
                response = "Wrong protocol"
                client_socket.recv(1024)  # Attempt to empty the socket from possible garbage

            client_socket.send(response.encode())

            if response.upper() == "EXIT":
                print(f"Closing connection...")
                break
    except ConnectionResetError:
        print("Connection was reset by the client")

    print("Connection closed\n")
    client_socket.close()
    server_socket.close()

if __name__ == "__main__":
    main()
