import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_addr = ('127.0.0.1', 55558)
client_socket.connect(server_addr)

client_socket.send("!!!".encode())
client_socket.send("111".encode())
client_socket.send("222".encode())
client_socket.send("333".encode())
client_socket.send("444".encode())
client_socket.send("close".encode())

client_socket.close()
