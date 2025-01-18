import os.path
import socket

def send_response(client_socket: socket.socket, request_message):
    valid_actions = ["GET"]
    (action, url, version) = request_message.split("\n")[0].split(" ")
    status = (200, "OK")
    file_length = 0
    content_type = "text/plain"
    response_content = b""
    read_mode = "r"
    forbidden_files = ["secret.txt"]

    content_type_map = {
        "html": "text/html; charset=utf-8",
        "js": "text/javascript; charset=UTF-8",
        "css": "text/css",
        "txt": "text/plain",
        "jpg": "image/jpeg",
        "png": "image/png"
    }

    if action not in valid_actions:
        status = (405, "Method Not Allowed")

    if url == "/":
        index_html_path = "index.html"
        if os.path.exists(index_html_path):
            with open(index_html_path, "r") as file:
                file_content = file.read()
                file_length = len(file_content)
                content_type = "text/html; charset=utf-8"
                response_content = file_content
        else:
            status = (404, "Not Found")
    else:
        file_name = url.lstrip("/") # / -> \
        if file_name in forbidden_files:
            client_socket.send("HTTP/1.1 403 Forbidden\r\n\r\n".encode())
            return

        file_extension = file_name.split(".")[-1]

        if file_extension in ["js", "css", "txt"]:
            read_mode = "r"
        else:
            read_mode = "rb" # Photos: jpg, png and so on...

        if os.path.exists(file_name):
            with open(file_name, read_mode) as file:
                file_content = file.read()
                file_length = len(file_content)

                content_type = content_type_map.get(file_extension, "text/plain")
                response_content = file_content
        else:
            status = (404, "Not Found")

    if read_mode == "r":
        response = (
           f"{version} {status[0]} {status[1]}\r\n"
           f"Content-Length: {file_length}\r\n"
           f"Content-Type: {content_type}\r\n"
           "\r\n"
           f"{response_content}"
        ).encode() # For text as string
    else:
        response = (
            f"{version} {status[0]} {status[1]}\r\n"
            f"Content-Length: {file_length}\r\n"
            f"Content-Type: {content_type}\r\n"
            "\r\n"
        ).encode() + response_content # For photos as bytes

    client_socket.send(response)

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 8080))
    server_socket.listen()
    print("Server is listening on 127.0.0.1...")

    try:
        while True:
            (client_socket, client_address) = server_socket.accept()
            print("Client connected. Please wait a few minutes for the website to load in the browser.")

            try:
                while True:
                    data = client_socket.recv(1024).decode()
                    if not data:
                        break

                    (request_type, url, version) = data.split("\r\n")[0].split(" ")

                    if request_type == "GET" and "/" in url and version.startswith("HTTP/"):
                        send_response(client_socket, data.split("\r\n")[0])
                    else:
                        client_socket.send("HTTP/1.1 405 Method Not Allowed\r\n\r\n".encode())
                        break

            except Exception as e:
                client_socket.send(f"HTTP/1.1 500 Internal Server Error\r\n\r\n{e}".encode())

    except KeyboardInterrupt:
        server_socket.close()
        print("Server is closed")

if __name__ == "__main__":
    main()