# Daniel Reiman
# 2024-12-28

import  socket

HOST = "0.0.0.0"
PORT = 8800

def create_http_response(status_code, status_message, content):
    request = (
        f"HTTP/1.1 {status_code} {status_message}\r\n"
        "Content-Type: text/plain\r\n"
        "\r\n"
        f"{content}"
    )

    return  request
def main():
   try:
       with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
           server_socket.bind((HOST, PORT))
           server_socket.listen()
           print("NOTE: This server project will automatically close after handling one client.")
           print(f"Server is listening...")

           (client_socket, client_address) = server_socket.accept()
           with client_socket:
               print(f"Connected to {client_address}")
               client_request = client_socket.recv(1024).decode('utf-8')
               print("\nClient request:")
               print(client_request)

               if client_request.split("\r\n")[0].split(" ")[0] == "GET":
                   server_response = create_http_response(200, "Ok", "This is pre 4.4 exercise")
                   client_socket.send(server_response.encode('utf-8'))
               else:
                   server_response = create_http_response(400, "Bad Request",
                                                          "Unsupported action:")
                   client_socket.send(server_response.encode('utf-8'))

               print("\nResponse sent successfully!")
   except Exception as e:
       print(e)



if __name__ == "__main__":
    main()

