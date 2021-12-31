# CS对接协议

## 控制报文（上发）
### 增加用户
```json
{'type': 'control', 'action': 'user_add', 'x': 8, 'y': 8, 'id': 2, 'name': 'dark'}
```
### 删除用户
```json
{'id': 2, 'type': 'control', 'action': 'user_remove'}
```
### 用户移动
> 往上移动
```json
{'type': 'control', 'action': 'user_move', 'id': 2, 'direction': 'up'}
```
> 往下移动
```json
{'type': 'control', 'action': 'user_move', 'id': 2, 'direction': 'down'}
```
> 往左移动
```json
{'type': 'control', 'action': 'user_move', 'id': 2, 'direction': 'left'}
```
> 往右移动
```json
{'type': 'control', 'action': 'user_move', 'id': 2, 'direction': 'right'}
```
### 子弹射击
> 往上射击
```json
{'type': 'control', 'action': 'bullet_shoot', 'id': 2, 'direction': 'up'}
```
> 往下射击
```json
{'type': 'control', 'action': 'bullet_shoot', 'id': 2, 'direction': 'down'}
```
> 往左射击
```json
{'type': 'control', 'action': 'bullet_shoot', 'id': 2, 'direction': 'left'}
```
> 往右射击
```json
{'type': 'control', 'action': 'bullet_shoot', 'id': 2, 'direction': 'right'}
```

## map显示报文（下发）
> 服务端收到任何type为control的报文都会广播map报文来刷新客户端显示
> 子弹刷新线程会在有子弹的情况下1s一次下发
```json
{'type': 'map', 'width': 20, 'height': 10, 'map_base': [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]}
```
