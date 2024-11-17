"""EX 2.6 client implementation
   Author: Daniel Reiman
   Date:
"""

import socket
import protocol


def main():
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect(("127.0.0.1", protocol.PORT))

    while True:
        user_input = input("Enter command\n")
        valid_cmd = protocol.check_cmd(user_input)

        if valid_cmd:
            message = protocol.create_msg(user_input)

            my_socket.send(message.encode())

            if user_input.upper() == "EXIT":
                break

            (success, content) = protocol.get_msg(my_socket)
            if success:
                print(content)
            else:
                print(f"Error: {content}")

        else:
            print("Not a valid command")

    print("Closing\n")
    my_socket.close()


if __name__ == "__main__":
    main()