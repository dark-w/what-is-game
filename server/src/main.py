from json.decoder import JSONDecodeError
import socket
import collections
import threading
import logger
import json
import yaml
import time
import os
import pdb

import server_env


class user:
    def __init__(self, name, id, v, x, y) -> None:
        self.x = x
        self.y = y
        self.v = v

        self.name = name
        self.id = id


class map:
    def __init__(self, config_fn: str) -> None:
        # objs
        self.users = []

        # map init
        with open(config_fn, 'r', encoding='utf-8') as config_file:
            map_data: map = yaml.safe_load(config_file)
            map_root = map_data.get('map')
            self.map_width = map_root.get('width')
            self.map_height = map_root.get('height')

            map_values = map_root.get('values')
            self.map_values_line_point = map_values.get('line')
            self.map_values_bg_point = map_values.get('bg')
            self.map_values_user_0 = map_values.get('user-0')

            self.map_base = []
            for i in range(self.map_height):
                temp = []
                for j in range(self.map_width):
                    temp.append(self.map_values_bg_point)
                self.map_base.append(temp)

            map_lines = map_root.get('lines')
            for line in map_lines:
                src_point = line.get('src')
                dst_point = line.get('dst')
                if src_point[0] == dst_point[0]:
                    small = src_point[1] if src_point[1] < dst_point[1] else dst_point[1]
                    big = src_point[1] if src_point[1] > dst_point[1] else dst_point[1]
                    for i in range(small, big + 1):
                        # print(i)
                        self.map_base[i][src_point[0]
                                         ] = self.map_values_line_point
                else:
                    small = src_point[0] if src_point[0] < dst_point[0] else dst_point[0]
                    big = src_point[0] if src_point[0] > dst_point[0] else dst_point[0]
                    for i in range(small, big + 1):
                        # print(i)
                        self.map_base[src_point[1]
                                      ][i] = self.map_values_line_point

    def user_add(self, user: user):
        self.users.append(user)
        if self.map_base[user.x][user.y] == self.map_values_bg_point:
            self.map_base[user.x][user.y] += user.v

    def user_remove(self, user: user):
        if user in self.users:
            self.users.remove(user)
            self.map_base[user.x][user.y] -= user.v

    def user_move(self, direction, user):
        # pdb.set_trace()
        if direction == 'up':
            if self.map_base[user.x + 1][user.y] == self.map_values_bg_point:
                self.map_base[user.x][user.y] -= user.v
                user.x += 1
                self.map_base[user.x][user.y] += user.v
        elif direction == 'down':
            if self.map_base[user.x - 1][user.y] == self.map_values_bg_point:
                self.map_base[user.x][user.y] -= user.v
                user.x -= 1
                self.map_base[user.x][user.y] += user.v
        elif direction == 'left':
            if self.map_base[user.x][user.y - 1] == self.map_values_bg_point:
                self.map_base[user.x][user.y] -= user.v
                user.y -= 1
                self.map_base[user.x][user.y] += user.v
        elif direction == 'right':
            if self.map_base[user.x][user.y + 1] == self.map_values_bg_point:
                self.map_base[user.x][user.y] -= user.v
                user.y += 1
                self.map_base[user.x][user.y] += user.v
    # TODO

    def loop(self):
        pass

    def debug_show(self):
        os.system('clear')
        print()
        for i in self.map_base:
            for j in i:
                print(j, end='')
            print()
        print()

    # FIXME: lock
    def dumps(self) -> str:
        retval = collections.OrderedDict()
        retval['type'] = 'map'
        retval['width'] = self.map_width
        retval['height'] = self.map_height
        retval['map_base'] = self.map_base
        return json.dumps(retval)


class server:
    def __init__(self) -> None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = (server_env.IP, server_env.PORT)
        self.logger = logger.log
        self.clients = []
        self.map = map('demo.yaml')

    def __map_data_broadcast(self):
        while True:
            pass

    def start(self):
        self.socket.bind(self.addr)
        self.logger.info("bind ok")

        self.socket.listen(5)
        self.logger.info("listen ok")

        thread_map_data_broadcast = threading.Thread(
            target=self.__map_data_broadcast, daemon=True)
        thread_map_data_broadcast.start()

        self.__broadcast_map()

        while True:
            self.logger.info("accepting...")
            client_socket, client_addr = self.socket.accept()
            self.clients.append((client_socket, client_addr))
            self.logger.info("accept a client")

            thread = threading.Thread(
                target=self.__handle, args=(client_socket, client_addr), daemon=True)
            thread.start()

    def __handle(self, client_socket: socket.socket, client_addr):
        __handle_user = user('null', -1, -1, -1, -1)
        while True:
            try:
                data = client_socket.recv(1024)

                if 0 == len(data):
                    break

                data_json = json.loads(data)
                self.logger.info(data_json)

                data_type = data_json.get('type')
                # {'type': 'control', 'action': 'user_move', 'id': 1, 'direction': 'up'}
                if data_type == 'control':
                    # pdb.set_trace()
                    data_action = data_json.get('action')
                    if data_action == 'user_add':
                        __handle_user.name = data_json.get('name')
                        __handle_user.id = data_json.get('id')
                        __handle_user.x = data_json.get('x')
                        __handle_user.y = data_json.get('y')
                        __handle_user.v = self.map.map_values_user_0

                        self.map.user_add(__handle_user)
                    elif data_action == 'user_move':
                        data_direction = data_json.get('direction')
                        data_id = data_json.get('id')
                        if data_id == __handle_user.id:
                            self.map.user_move(data_direction, __handle_user)
                    elif data_action == 'user_remove':
                        data_id = data_json.get('id')
                        if data_id == __handle_user.id:
                            self.map.user_remove(__handle_user)

                self.__broadcast_map()
            except Exception as e:
                self.logger.error(e.args)
                break

        self.logger.info("client close")
        self.clients.remove((client_socket, client_addr))
        self.map.user_remove(__handle_user)
        client_socket.close()

    def __broadcast_not_myself(self, myself_sock, data):
        for sock, addr in self.clients:
            if myself_sock != sock:
                sock.send(data)

    def __broadcast_map(self):
        map_data = self.map.dumps()
        for sock, addr in self.clients:
            sock.send(map_data.encode())


if __name__ == '__main__':
    s = server()
    s.start()
