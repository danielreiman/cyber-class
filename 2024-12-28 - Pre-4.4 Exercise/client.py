# Daniel Reiman
# 2024-12-28

import socket as socket

HOST = "127.0.0.1"
PORT = 8800

def create_http_request_client(method, url):
    request = (
        f"{method} {url} HTTP/1.1\r\n"
        f"Host: {HOST}\r\n"
        "Accept: text/plain"
    )

    return  request

def main():
   with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
       try:
           client_socket.connect((HOST, PORT))
           print("NOTE: This server project will automatically close after handling one client.")
           user_input = input("Type GET in order to get a message from the server: ")
           if user_input.upper() == "GET":
               request = create_http_request_client("GET", "/").encode('utf-8')
               client_socket.send(request)
               print("Request sent successfully to the HTTP server\n")

               response = client_socket.recv(1024).decode('utf-8')
               print("Server response:")
               print(f"{response}")
               print(f"Message: {response.split("\n\r")[-1]}")
           else:
               print("Unknown command")
       except Exception as e:
           print(e)


if __name__ == "__main__":
    main()
