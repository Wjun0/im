# 1，协程打补丁，将IO操作变为异步
from eventlet import monkey_patch
monkey_patch()

import socketio
# 2，创建socketio服务器
sio = socketio.Server(async_model='eventlet')

# sio = socketio.AsyncServer()
# app = socketio.ASGIApp(sio)
# app = socketio.WSGIApp(sio,app)

# 3，创建应用，管理im服务器
app = socketio.Middleware(sio)

# 4，监听端口
import eventlet.wsgi
sock = eventlet.listen(('192.168.59.129',9000))


@sio.event
def connect(sid,environ):
    print('连接时自动调用')
    print('+++',sid,environ)


@sio.event
def disconnect(sid):
    print('断开连接时调用',sid)


@sio.on('message')
def message(sid,data):
    print(sid)
    print('接收到的信息是：',data)
    sio.emit('message','你好啊！',room=sid)



#5启动app
eventlet.wsgi.server(sock,app)
