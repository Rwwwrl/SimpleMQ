import socket
import json

sock = socket.socket()
sock.connect(('localhost', 9090))

data = {
    'type': 'publisher',
    'data': 'hello world!',
}

data_as_bytes = json.dumps(data).encode('utf-8')

sock.send(data_as_bytes)

sock.close()
