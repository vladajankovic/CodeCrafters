import socket
import threading
import argparse
import os

def handle_request(client_socket : socket.socket, directory=None):
    data = client_socket.recv(1024).decode()
    data = data.split("\r\n")

    startline = data[0].split(" ")
    method = startline[0]
    path = startline[1]
    http_version = startline[2]

    if method == "GET":
        if path == "/":
            client_socket.send('{} 200 OK\r\n\r\n'.format(http_version).encode())
        
        elif path[:6] == '/echo/':
            text = path[6:]
            client_socket.send(f'{http_version} 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(text)}\r\n\r\n{text}'.encode())
        
        elif path == '/user-agent':  
            useragent = data[2].split()[1]
            client_socket.send(f'{http_version} 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(useragent)}\r\n\r\n{useragent}'.encode())
        
        elif path[:7] == '/files/':
            filename = path[7:]
            filepath = f'{directory}/{filename}'
            exists = os.path.exists(filepath)
            if exists:
                with open(filepath, 'r') as f:
                    text = f.read()
                    client_socket.send(f'{http_version} 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {len(text)}\r\n\r\n{text}'.encode())
            else:
                client_socket.send(f'{http_version} 404 Not Found\r\nContent-Length: 0\r\n\r\n'.encode())
        
        else:
            client_socket.send(f'{http_version} 404 Not Found\r\n\r\n'.encode())
    
    else:   # POST method
        text = data[-1]
        filename = path[7:]
        filepath = f'{directory}/{filename}'
        with open(filepath, 'w') as f:
            f.write(text)
        client_socket.send(f'{http_version} 201 Created\r\n\r\n'.encode())

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--directory')
    args = parser.parse_args()
    directory = args.directory

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    while True:
        try:
            client_socket, client = server_socket.accept() # wait for client

            client_thread = threading.Thread(target=handle_request, args=(client_socket, directory))
            client_thread.start()
            
        except TimeoutError:
            break


if __name__ == "__main__":
    main()
