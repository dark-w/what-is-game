import socket
import collections
import threading
import logger

class server:
    def __init__(self) -> None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = ('10.0.12.11', 55558)
        self.logger = logger.log

    def start(self):
        self.socket.bind(self.addr)
        self.logger.info("bind ok")

        self.socket.listen(5)
        self.logger.info("listen ok")

        while True:
            self.logger.info("accepting...")
            client_socket, client_addr = self.socket.accept()
            self.logger.info("accept a client")

            thread = threading.Thread(target=self.__handle, args=(client_socket, client_addr))
            thread.start()

    def __handle(self, client_socket: socket.socket, client_addr):
        while True:
            try:
                data = client_socket.recv(1024)

                if 0 == len(data):
                    break

                data_str = data.decode()
                self.logger.debug(data_str)

                if data_str == 'close':
                    break
            except:
                break

        self.logger.info("client close")
        client_socket.close()

if __name__ == '__main__':
    s = server()
    s.start()
        
