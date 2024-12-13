import socket
import protocol
import base64
from PIL import Image

from protocol import check_cmd


def get_image(my_socket: socket.socket):
    full_data = ""
    while True:
        success, content = protocol.get_msg(my_socket)
        if not success:
            print("Error receiving data from server.")
            return
        if content == "END_OF_FILE":
            break
        full_data += content

    try:
        # Add padding
        if len(full_data) % 4 != 0:
            full_data += "=" * (4 - len(full_data) % 4)

        # Convert string to data
        data = base64.b64decode(full_data)

        filename = "received_image.png"
        with open(filename, "wb") as file:
            file.write(data)

        print(f"Image received and saved as {filename}")

        with Image.open(filename) as img:
            img.show()
    except Exception as error:
        print(f"Error: {error}")


def print_menu():
    print("\nAvailable Commands:")
    print("1. TAKE_SCREENSHOT <path> - Takes a screenshot and saves it to the specified path.")
    print("2. SEND_FILE <file_path> - Sends the specified file to the server.")
    print("3. DIR <directory_path> - Lists all files in the specified directory.")
    print("4. DELETE <file_path> - Deletes the specified file.")
    print("5. COPY <source_path> <destination_path> - Copies a file from the source to the destination.")
    print("6. EXECUTE <file_path> - Executes the specified file.")
    print("7. EXIT - Closes the connection and exits the program.")

def main():
    try:
        my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        my_socket.connect(("127.0.0.1", protocol.PORT))
        print("Connected to the server.")

        while True:
            print_menu()
            user_input = input("Enter command:\n").strip()
            if not user_input:
                print("Command cannot be empty.")
                continue

            if " " in user_input:
                command, parameter = user_input.split(" ", 1)
            else:
                command = user_input
                parameter = None

            if parameter is None and check_cmd(command):
                print(f"The command '{command}' requires a parameter.")
                continue

            if command.upper() == "EXIT":
                print("Exiting...")
                break

            valid_cmd = protocol.check_cmd(command.upper())
            if valid_cmd:
                message = protocol.create_msg(user_input)
                my_socket.send(message.encode())

                if command.upper() == "SEND_FILE":
                    get_image(my_socket)

                    success, final_msg = protocol.get_msg(my_socket)
                    if success:
                        print(final_msg)
                    else:
                        print("Failed to receive final message")
                else:
                    success, content = protocol.get_msg(my_socket)
                    if success:
                        print(content)
                    else:
                        print("Error receiving response from server")
            else:
                print(f"'{command}' is not a valid command.")

        print("Closing connection...")
        my_socket.close()
        print("Connection closed.")
    except ConnectionRefusedError:
        print("Error: Unable to connect to the server. Ensure the server is running.")
    except BrokenPipeError:
        print("Error: Connection to the server was lost.")
    except Exception as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()