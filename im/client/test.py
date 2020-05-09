

import socketio

sio = socketio.Client()

sio.connect('http://192.168.59.129:9000')

@sio.event
def message(data):
    print(data)
    # sio.emit('message',{"ho":"hello"})

sio.emit('message',{"hozzz":"hello"})