# 协程：微线程，可以在同一个线程里面切换
# 场景：对于IO复杂（读写文件，网络数据读写）的任务，cpu长时间没有工作，

# 1，协程打补丁，将IO操作变为异步
from eventlet import monkey_patch
monkey_patch()

# 2，创建socketio服务器
import socketio
sio = socketio.Server(async_mode ='eventlet')

# 3，创建应用，管理im服务器
app = socketio.Middleware(sio)

# 4，监听端口
import eventlet.wsgi
sock = eventlet.listen(('192.168.59.129',9000))

# 添加两个默认事件：
@sio.on('connect')
def on_connect(sid,enciron):
    print('连接时自动触发')
    print(sid)
    sio.enter_room(sid,'wangjun')  #连接时自动进入房间，


@sio.on('disconnect')
def dis_connect(sid):
    print('断开连接时触发')
    #一旦断开连接应该离开所有的房间，
    rooms = sio.rooms(sid)
    for room in rooms:
        sio.leave_room(sid,room)



#自定义事件
@sio.on('wj') #wj事件名称
def test(sid,data):
    print('接收到的消息是：',data)
    #发送消息
    sio.emit('wj','再见')  #默认是群发消息
    sio.emit('wj','再见',room=sid)  #发给指定的人,单聊模式
    # room会作为房间的名称，在该房间的客服都能收到消息，进入房间可以用sio.enter_room(sid,'wangjun')
    sio.emit('wj','再见',room='wangjun')


#自定义离开房间事件
@sio.on('leave')
def on_deave(sid,data):
    sio.leave_room(sid,room='wangjun')


# 5，启动服务器
eventlet.wsgi.server(sock,app)

