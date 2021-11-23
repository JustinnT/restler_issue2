from os import error
import httpx
import socket 
import sys
import json

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 12345

def send_back_client(status_code, reason_phrase, headers, content, client_connection):

    response_headers = ''.join('%s: %s\r\n' % (k, v) for k, v in headers.items())
    response_protocol = 'HTTP/1.1'

    r = '%s %s %s\r\n' % (response_protocol, status_code, reason_phrase)
    r = (r + response_headers + '\r\n').encode() + content
    client_connection.sendall(r)

try:

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((SERVER_HOST, SERVER_PORT))
    s.listen(socket.SOMAXCONN)
    print(f"Server is listening on {SERVER_HOST} port {SERVER_PORT}\n")

except Exception as e:
    print(e)
    sys.exit(0)

while True:
    client_connection, client_address = s.accept()
    print("Got a connection from ", client_address)

    request = client_connection.recv(1024).decode()
    print(f"Restler sent:\n{request}")

    send_back_client('404', 'notfound', {}, b'', client_connection)

    client_connection.close()