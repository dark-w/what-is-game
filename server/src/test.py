import socket
import json
import collections

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_addr = ('127.0.0.1', 55558)
client_socket.connect(server_addr)

data = collections.OrderedDict()
data['x'] = 1
data['y'] = 2
data['type'] = 'user_location'
data['name'] = 'nick'
data['id'] = 0
data['netstat'] = 'on'
data_json = json.dumps(data)
client_socket.send(data_json.encode())

while True:
    recv_data = client_socket.recv(1024)
    recv_data_json = json.loads(recv_data)
    print(recv_data_json)

client_socket.close()
