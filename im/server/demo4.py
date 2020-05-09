
from eventlet import monkey_patch
monkey_patch()

import socketio
sio = socketio.Server(async_mode = 'eventlet')

app = socketio.Middleware(sio)

import eventlet.wsgi
sock = eventlet.listen(('192.168.59.129',9000))

#添加默认事件
@sio.on('connect')
async def test_connect(sid,environ):
    print('连接时自动调用')
    await sio.emit('my_response',{"data":'connected'})

@sio.on('disconnect')
async def test_disconnect(sid):
    print('连接时自动调用')
    await sio.emit('my_response',{"data":'disconnected'})


@sio.on('my_event')
async def send_message(sid,message):
    await sio.emit('my_event',{"data":"ok"})


eventlet.wsgi.server(sock,app)
