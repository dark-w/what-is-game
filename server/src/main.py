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
import copy
import queue

import server_env


class user:
    def __init__(self, name, id, v, x, y) -> None:
        self.x = x
        self.y = y
        self.v = v

        self.init_x = x
        self.init_y = y

        self.name = name
        self.id = id

        self.hp_full = 3
        self.hp_now = self.hp_full
        
class bullet:
    def __init__(self, user: user, direction, v) -> None:
        self.speed = 1
        self.damage = 1
        self.direction = direction
        self.v = v
        self.timer = time.time()

        self.user = user
        self.x = user.x
        self.y = user.y

        if direction == 'up':
            self.x += 1
        elif direction == 'down':
            self.x -= 1
        elif direction == 'left':
            self.y -= 1
        elif direction == 'right':
            self.y += 1

class map:
    def __init__(self, config_fn: str, server) -> None:
        self.server = server

        # objs
        self.users = []
        self.bullets = []

        self.map_operate_lock = threading.Lock()

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
            self.map_values_bullet_0 = map_values.get('bullet-0')

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
        self.map_operate_lock.acquire()

        if self.map_base[user.x][user.y] == self.map_values_bg_point:
            self.users.append(user)
            self.map_base[user.x][user.y] += user.v

        self.map_operate_lock.release()

    def user_remove(self, user: user):
        self.map_operate_lock.acquire()

        if user in self.users:
            self.users.remove(user)
            self.map_base[user.x][user.y] -= user.v

        self.map_operate_lock.release()

    def user_move(self, direction, user):
        self.map_operate_lock.acquire()

        x_value = 0
        y_value = 0
        if direction == 'up':
            x_value = 1
        elif direction == 'down':
            x_value = -1
        elif direction == 'left':
            y_value = -1
        elif direction == 'right':
            y_value = 1

        if self.map_base[user.x + x_value][user.y + y_value] == self.map_values_bg_point:
            self.map_base[user.x][user.y] -= user.v
            user.x += x_value
            user.y += y_value
            self.map_base[user.x][user.y] += user.v

        self.map_operate_lock.release()

    def user_teleport(self, user, x, y):
        self.map_operate_lock.acquire()

        if self.map_base[x][y] == self.map_values_bg_point:
            self.map_base[user.x][user.y] -= user.v
            user.x = x
            user.y = y
            self.map_base[user.x][user.y] += user.v

        self.map_operate_lock.release()

    def bullet_shoot(self, b: bullet):
        direction = b.direction
        if self.map_base[b.x][b.y] == self.map_values_bg_point:
            self.bullets.append(b)
            self.map_base[b.x][b.y] = b.v

    def bullets_loop(self):
        start_time = time.time()
        while True:
            if len(self.bullets) > 0:
                for b in self.bullets:
                    direction = b.direction
                    v = b.v
                    speed = b.speed
                    if time.time() - b.timer > speed / 20:
                        x_value = 0
                        y_value = 0
                        if direction == 'up':
                            x_value = 1
                        elif direction == 'down':
                            x_value = -1
                        elif direction == 'left':
                            y_value = -1
                        elif direction == 'right':
                            y_value = 1

                        if self.map_base[b.x + x_value][b.y + y_value] == self.map_values_bg_point:
                            self.map_base[b.x][b.y] -= v
                            b.x += x_value
                            b.y += y_value
                            self.map_base[b.x][b.y] += v
                        elif self.map_base[b.x + x_value][b.y + y_value] == self.map_values_line_point:
                            self.map_base[b.x][b.y] -= v
                            self.bullets.remove(b)
                        elif self.map_base[b.x + x_value][b.y + y_value] == self.map_values_user_0:
                            for u in self.users:
                                if u.x == b.x + x_value and u.y == b.y + y_value \
                                    and u.id != b.user.id:
                                    # bullet clean
                                    self.map_base[b.x][b.y] -= b.v
                                    self.bullets.remove(b)

                                    # user teleport
                                    self.user_teleport(u, u.init_x, u.init_y)

                                    break

                        self.server.broadcast_map()
                        b.timer = time.time()
                        

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

        # retval['map_base'] = self.map_base
        self.map_operate_lock.acquire()
        retval['map_base'] = copy.deepcopy(self.map_base)
        self.map_operate_lock.release()

        return json.dumps(retval)


class server:
    def __init__(self) -> None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = (server_env.IP, server_env.PORT)
        self.logger = logger.log
        self.clients = []
        self.map = map("{}/demo.yaml".format(server_env.GAME_SERVER_HOME), self)
        
    def start(self):
        self.socket.bind(self.addr)
        self.logger.info("bind ok")

        self.socket.listen(5)
        self.logger.info("listen ok")

        thread_bullets_loop = threading.Thread(
            target=self.map.bullets_loop, daemon=True)
        thread_bullets_loop.start()

        self.broadcast_map()

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
                data_id = data_json.get('id')
                
                if data_type == 'control':
                    data_action = data_json.get('action')
                    if data_action == 'user_add':
                        __handle_user.name = data_json.get('name')
                        __handle_user.id = data_json.get('id')
                        __handle_user.x = data_json.get('x')
                        __handle_user.y = data_json.get('y')
                        __handle_user.init_x = __handle_user.x
                        __handle_user.init_y = __handle_user.y
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
                    elif data_action == 'bullet_shoot':
                        data_id = data_json.get('id')
                        data_direction = data_json.get('direction')
                        if data_id == __handle_user.id:
                            b = bullet(__handle_user, data_direction, self.map.map_values_bullet_0)
                            self.map.bullet_shoot(b)

                self.broadcast_map()
            except Exception as e:
                self.logger.error(e.args)
                break

        self.logger.info("client close")
        self.clients.remove((client_socket, client_addr))
        self.map.user_remove(__handle_user)
        client_socket.close()

    def broadcast_map(self):
        # self.map.debug_show()
        map_data = self.map.dumps()
        for sock, addr in self.clients:
            try:
                sock.send((map_data + '\n').encode())
            except BrokenPipeError as e:
                self.logger.error(e.args) # FIXME
                continue


if __name__ == '__main__':
    s = server()
    s.start()
