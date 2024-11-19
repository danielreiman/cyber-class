"""EX 2.6 server implementation
   Author: Daniel Reiman
   Date:
"""

import socket
import protocol
from datetime import datetime
import random
from protocol import check_cmd

def create_server_rsp(cmd: str):
    server_name = "ProB"
    upper_cmd = cmd.upper()
    if upper_cmd == "TIME":
        current_time = datetime.now().strftime("%H:%M:%S")
        return current_time
    elif upper_cmd == "RAND":
        return str(random.randint(1, 99))
    elif upper_cmd == "EXIT":
        return "EXIT"
    elif upper_cmd == "NAME":
        return server_name
    return "Unknown command. Please check your input."


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", protocol.PORT))
    server_socket.listen()
    print("Server is up and running")
    (client_socket, client_address) = server_socket.accept()
    print("Client connected")

    try:
        while True:
            valid_msg, cmd = protocol.get_msg(client_socket)
            if valid_msg:
                print(cmd)
                if check_cmd(cmd):
                    response = protocol.create_msg(create_server_rsp(cmd))
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
