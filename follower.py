import socket
import json

sock = socket.socket()
sock.connect(('localhost', 9090))

data = {
    'type': 'follower',
}

data_as_bytes = json.dumps(data).encode('utf-8')

sock.send(data_as_bytes)

while True:
    data = sock.recv(1024)
    print('here some data')
    print(data)
    if not data:
        break

sock.close()
