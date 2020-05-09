#同时多个房间聊天

# 协程：微线程，可以在同一个线程里面切换
# 场景：对于IO复杂（读写文件，网络数据读写）的任务，cpu长时间没有工作，

# 1，协程打补丁，将IO操作变为异步
from eventlet import monkey_patch
monkey_patch()

# 2，创建socketio服务器
import socketio
sio = socketio.Server(async_model='eventlet')

# 3，创建应用，管理im服务器
app = socketio.Middleware(sio)

# 4，监听端口
import eventlet.wsgi
sock = eventlet.listen(('192.168.59.129',9000))



# 添加两个默认事件：
@sio.on('connect')
def on_connect(sid,environ):
    print('连接时自动触发')
    print(sid)
    print(environ)   #字典形式，http连接时的信息，token等
    # sio.enter_room(sid,'room1')
    # sio.enter_room(sid,'room2')



@sio.on('disconnect')
def dis_connect(sid):
    print('断开连接时触发')
    #一旦断开连接应该离开所有的房间，
    rooms = sio.rooms(sid)
    print(rooms)
    for room in rooms:
        sio.leave_room(sid,room)


# 自定义事件
@sio.on('event_1') #wj事件名称
def test(sid,data):
    print('接收到的消息是：',data)
    #发送消息
    # sio.emit('wj','再见')  #默认是群发消息
    # sio.emit('wj','再见',room=sid)  #发给指定的人,单聊模式
    # room会作为房间的名称，在该房间的客服都能收到消息，进入房间可以用sio.enter_room(sid,'wangjun')
    room = data.get('room')     #根据收到的消息判断是那房间的聊天信息，对应回复那个房间。
    sio.enter_room(sid, room)   #先进入房间
    sio.emit('event_1','再见',room=room)
    # sio.emit('event_1','再见2',room='room2')



#自定义离开房间事件
@sio.on('leave')
def on_leave(sid,data):
    sio.leave_room(sid,room='wangjun')


# 5，启动服务器
eventlet.wsgi.server(sock,app)


