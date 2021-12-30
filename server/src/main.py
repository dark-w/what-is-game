from json.decoder import JSONDecodeError
import socket
import collections
import threading
import logger
import json

import server_env


class server:
    def __init__(self) -> None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = (server_env.IP, server_env.PORT)
        self.logger = logger.log
        self.clients = []

    def start(self):
        self.socket.bind(self.addr)
        self.logger.info("bind ok")

        self.socket.listen(5)
        self.logger.info("listen ok")

        while True:
            self.logger.info("accepting...")
            client_socket, client_addr = self.socket.accept()
            self.clients.append((client_socket, client_addr))
            self.logger.info("accept a client")

            thread = threading.Thread(
                target=self.__handle, args=(client_socket, client_addr))
            thread.start()

    def __handle(self, client_socket: socket.socket, client_addr):
        while True:
            try:
                data = client_socket.recv(1024)

                if 0 == len(data):
                    break

                data_json = json.loads(data)
                self.logger.info(data_json)

                # {name: "nick", id: 0, x: 0, y: 1, netstat: "on"，type: "user_location"}
                data_name = data_json.get('name')
                data_id = data_json.get('id')
                data_x = data_json.get('x')
                data_y = data_json.get('y')
                data_netstat = data_json.get('netstat')
                data_type = data_json.get('type')

                if data_type == 'user_location':
                    self.logger.info("after resolved: name: {} id: {} x: {} y: {} netstat: {} type: {}".format(
                        data_name, data_id, data_x, data_y, data_netstat, data_type
                    ))
                    self.__broadcast_not_myself(client_socket, data)

            except:
                self.logger.error("server::__handle exception")
                break

        self.logger.info("client close")
        self.clients.remove((client_socket, client_addr))
        client_socket.close()

    def __broadcast_not_myself(self, myself_sock, data):
        for sock, addr in self.clients:
            if myself_sock != sock:
                sock.send(data)

if __name__ == '__main__':
    s = server()
    s.start()
