import socket
import json
import collections
import sys
import threading
import os
import signal

import server_env


if len(sys.argv) != 4:
    print("usage: python test.py id x y\n"
          "example: python test.py 1 8 8")
    exit(-1)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_addr = ('127.0.0.1', server_env.PORT)
server_addr = ('150.158.214.239', server_env.PORT)


client_socket.connect(server_addr)

def display_func():
    while True:
        data_recv = client_socket.recv(4096)
        data_recv_json = json.loads(data_recv)

        type = data_recv_json.get('type')
        if type == 'map':
            map_base = data_recv_json.get('map_base')
            os.system('clear')
            print()
            for i in map_base:
                for j in i:
                    if j == 0:
                        print(' ', end="")
                    elif j == 1:
                        print('*', end="")
                    elif j == 2:
                        print('O', end="")
                    elif j == 3:
                        print('.', end="")
                print()
            print()


thread_display = threading.Thread(
    target=display_func, daemon=True)
thread_display.start()

# user add
user_add_data = collections.OrderedDict()
user_add_data['type'] = 'control'
user_add_data['action'] = 'user_add'
user_add_data['x'] = int(sys.argv[2])
user_add_data['y'] = int(sys.argv[3])
user_add_data['id'] = int(sys.argv[1])
user_add_data['name'] = 'dark'
user_add_data_json = json.dumps(user_add_data)
client_socket.send(user_add_data_json.encode())

user_remove_data = collections.OrderedDict()
user_remove_data['id'] = user_add_data['id']
user_remove_data['type'] = 'control'
user_remove_data['action'] = 'user_remove'
user_remove_data_json = json.dumps(user_remove_data)


def exit_callback(signum, frame):
    print('You choose to stop me.')
    client_socket.send(user_remove_data_json.encode())
    client_socket.close()
    exit(0)


signal.signal(signal.SIGINT, exit_callback)
signal.signal(signal.SIGTERM, exit_callback)

# user move
user_move_data = collections.OrderedDict()
user_move_data['type'] = 'control'
user_move_data['action'] = 'user_move'
user_move_data['id'] = user_add_data['id']

# bullet shoot
user_bullet_shoot_data = collections.OrderedDict()
user_bullet_shoot_data['type'] = 'control'
user_bullet_shoot_data['action'] = 'bullet_shoot'
user_bullet_shoot_data['id'] = user_add_data['id']

user_move_key = ['w', 's', 'a', 'd']
bullet_shoot_key = ['i', 'k', 'j', 'l']


while True:
    input_str = input()
    # input_str = sys.stdin.read(1)
    if input_str in user_move_key:
        if input_str == 'w':
            user_move_data['direction'] = 'up'
        elif input_str == 's':
            user_move_data['direction'] = 'down'
        elif input_str == 'a':
            user_move_data['direction'] = 'left'
        elif input_str == 'd':
            user_move_data['direction'] = 'right'

        user_move_data_json = json.dumps(user_move_data)
        client_socket.send(user_move_data_json.encode())
    elif input_str in bullet_shoot_key:
        if input_str == 'i':
            user_bullet_shoot_data['direction'] = 'up'
        elif input_str == 'k':
            user_bullet_shoot_data['direction'] = 'down'
        elif input_str == 'j':
            user_bullet_shoot_data['direction'] = 'left'
        elif input_str == 'l':
            user_bullet_shoot_data['direction'] = 'right'

        bullet_shoot_data_json = json.dumps(user_bullet_shoot_data)
        client_socket.send(bullet_shoot_data_json.encode())
    elif input_str == 'q':
        break
client_socket.send(user_remove_data_json.encode())
client_socket.close()
