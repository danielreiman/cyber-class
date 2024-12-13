
import os
import socket
import protocol
import pyautogui
from protocol import check_cmd
import base64
import glob
import shutil
import subprocess

def take_screenshot(parameter: str):
    screenshot = pyautogui.screenshot()
    screenshot.save(os.path.join(parameter, "screenshot.png"))

def send_data_as_parts(data: str, client_socket: socket.socket, size_of_each_part: int = 1024):
    for i in range(0, len(data), size_of_each_part):
        data_part = data[i: i + size_of_each_part]
        client_socket.send(protocol.create_msg(data_part).encode())

    client_socket.send(protocol.create_msg("END_OF_FILE").encode())

def send_photo(image_path: str, client_socket: socket.socket):
    try:
        if not os.path.exists(image_path):
            client_socket.send(protocol.create_msg(f"Error: '{image_path}' does not exist.").encode())

        with open(image_path, "rb") as image:
            data = image.read()
            encoded_data = base64.b64encode(data).decode('utf-8')  # Convert to string
            send_data_as_parts(encoded_data, client_socket)  # Send encoded data in parts
        print("Image sent successfully")
    except FileNotFoundError:
        client_socket.send(protocol.create_msg("File not found").encode())
    except Exception as error:
        client_socket.send(protocol.create_msg(f"Error: {str(error)}").encode())

def send_dir(path: str, client_socket: socket):
    files_list = glob.glob(path + "/*")
    files_string = ""

    for line in files_list:
        files_string += line + "\n"

    client_socket.send(protocol.create_msg(files_string).encode())

def delete_file(path: str, client_socket: socket):
    try:
        os.remove(fr"{path}")
    except FileNotFoundError:
        client_socket.send(protocol.create_msg(f"Error: No such file or directory: '{path}'").encode())
    except Exception as error:
        client_socket.send(protocol.create_msg(f"Error: {error}").encode())

def copy(parameter: str, client_socket: socket.socket):
    try:
        paths = parameter.split(" ", 1)
        if len(paths) < 2:
            client_socket.send(protocol.create_msg("Error: Source and destination paths must be provided").encode())
            return

        source, destination = paths

        if not os.path.isfile(source):
            client_socket.send(protocol.create_msg(f"Error: Source file '{source}' does not exist.").encode())
            return

        shutil.copy(source, destination)
        client_socket.send(protocol.create_msg("File copied successfully").encode())
    except FileNotFoundError:
        client_socket.send(protocol.create_msg("Error: File not found").encode())
    except Exception as error:
        client_socket.send(protocol.create_msg(f"Error: {error}").encode())

def execute(parameter, client_socket: socket):
    try:
        if not os.path.exists(parameter):
            client_socket.send(protocol.create_msg(f"The file '{parameter}' does not exist.").encode())

        # For macos
        # subprocess.call(["open", parameter])

        # For windows
        subprocess.call(f'start "" "{parameter}"')

        client_socket.send(protocol.create_msg("Command executed successfully").encode())
    except Exception as error:
        client_socket.send(protocol.create_msg(f"Error: {error}").encode())

def create_server_rsp(cmd: str, parameter: str, client_socket: socket):
    cmd = cmd.upper()
    match cmd:
        case "TAKE_SCREENSHOT":
            take_screenshot(parameter)
            client_socket.send(protocol.create_msg("The screenshot has been successfully captured and stored.").encode())
        case "SEND_FILE":
            send_photo(parameter, client_socket)
            client_socket.send(protocol.create_msg("The screenshot has been successfully sent from the server.").encode())
        case "DIR":
            send_dir(parameter, client_socket)
        case "DELETE":
            delete_file(parameter, client_socket)
            client_socket.send(protocol.create_msg("The screenshot has been successfully sent from the server.").encode())
        case "COPY":
            copy(parameter, client_socket)
        case "EXECUTE":
            execute(parameter, client_socket)
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
            valid_msg, message = protocol.get_msg(client_socket)

            if " " in message:
                cmd, parameter = message.split(" ", 1)
            else:
                cmd = message.strip()
                parameter = None

            if parameter is None and check_cmd(cmd):
                continue

            print(f"Received command: {cmd}, parameter: {parameter}")
            if valid_msg:
                if check_cmd(cmd):
                    create_server_rsp(cmd, parameter, client_socket)
                else:
                    client_socket.send(protocol.create_msg("Wrong command").encode())
            else:
                client_socket.send(protocol.create_msg("Wrong protocol").encode())

                client_socket.recv(1024)  # Attempt to empty the socket from possible garbage


            if cmd.upper() == "EXIT":
                print(f"Closing connection...")
                break
    except ConnectionResetError:
        print("Connection was reset by the client")

    print("Connection closed\n")
    client_socket.close()
    server_socket.close()

if __name__ == "__main__":
    main()
