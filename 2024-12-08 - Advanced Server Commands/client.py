"""EX 2.6 client implementation
   Author: Daniel Reiman
   Date:
"""

import socket
import protocol

def main():
    try:
        my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        my_socket.connect(("127.0.0.1", protocol.PORT))

        while True:
            user_input = input("Enter command\n")
            has_parameter = True
            if not (len(user_input.split(" ")) > 1):
                command = user_input
                has_parameter = False
            else:
                (command, parameter) = user_input.split(" ")

            valid_cmd = protocol.check_cmd(command)

            if valid_cmd and has_parameter:
                message = protocol.create_msg(user_input)

                my_socket.send(message.encode())

                (success, content) = protocol.get_msg(my_socket)
                if success:
                    print(content)
                else:
                    print(f"Error: {content}")
            elif valid_cmd and not has_parameter:
                print(f"The command {command} is missing 1 parameter")
            elif command.upper() == "EXIT":
                break
            else:
                print("Not a valid command")

        print("Closing")
        my_socket.close()
        print("Connection closed\n")
    except ConnectionRefusedError:
        print("Please ensure the server is running")
    except BrokenPipeError:
        print("Error: Connection to the server was lost.")

if __name__ == "__main__":
    main()
