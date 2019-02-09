其余部分未改动.

1.使用pip freeze > requirements.txt来自动生成pip安装目录

2.使用dwebsocket实现聊天,在这里没有使用通道,所以不需要redis作为媒介,也不需要routing等通道文件

    实现原理:(WebSocket协议由RFC 6455定义)
    WebSocket用于在Web浏览器和服务器之间进行任意的双向数据传输的一种技术。
    WebSocket协议基于TCP协议实现，包含初始的握手过程，以及后续的多次数据帧双向传输过程。
    其目的是在WebSocket应用和WebSocket服务器进行频繁双向通信时，可以使服务器避免打开多个HTTP连接进行工作来节约资源，提高了工作效率和资源利用率。

    WebSocket技术的优点有：
    1）通过第一次HTTP Request建立了连接之后，后续的数据交换都不用再重新发送HTTP Request，节省了带宽资源；
    2) WebSocket的连接是双向通信的连接，在同一个TCP连接上，既可以发送，也可以接收;
    3)具有多路复用的功能(multiplexing)，也即几个不同的URI可以复用同一个WebSocket连接。
    这些特点非常类似TCP连接，但是因为它借用了HTTP协议的一些概念，所以被称为了WebSocket。

    websocket客户端接口API:接口的内容可以分为三类：状态变量、网络功能和消息处理等。
    构造函数WebSocket(url, protocols)：构造WebSocket对象，以及建立和服务器连接; protocols可选字段，代表选择的子协议
    状态变量readyState: 代表当前连接的状态，短整型数据，取值为CONNECTING(值为0)， OPEN(值为1), CLOSING(值为2), CLOSED(值为3)
    方法变量close(code, reason)： 关闭此WebSocket连接。
    状态变量bufferedAmount: send函数调用后，被缓存并且未发送到网络上的数据长度
    方法变量send(data): 将数据data通过此WebSocket发送到对端
    回调函数onopen/onmessage/onerror/onclose: 当相应的事件发生时会触发此回调函数
    (JavaScript)
        var websocket = new WebSocket("ws://www.host.com/path");    //WebSocket连接服务器的URI以"ws"或者"wss"开头。ws开头的默认TCP端口为80，wss开头的默认端口为443。
        websocket.onopen = function(evt) { onOpen(evt) };
        websocket.onclose = function(evt) { onClose(evt) };
        websocket.onmessage = function(evt) { onMessage(evt) };
        websocket.onerror = function(evt) { onError(evt) }; }
        function onMessage(evt) { alert( evt.data); }
        function onError(evt) { alert( evt.data); }
        websocket.send("client to server");

    (python)
       使用上很方便,如果为一个单独的视图函数处理一个websocklet连接可以使用accept_websocket装饰器，它会将标准的HTTP请求路由到视图中。
       使用require_websocke装饰器只允许使用WebSocket连接，会拒绝正常的HTTP请求。
        在设置中添加设置MIDDLEWARE_CLASSES=dwebsocket.middleware.WebSocketMiddleware这样会拒绝单独的视图实用websocket，必须加上accept_websocket 装饰器。
        设置WEBSOCKET_ACCEPT_ALL=True可以允许每一个单独的视图实用websockets.....当然,在settings中这样做完全没必要

    一些属性和方法
        1.request.is_websocket()
        如果是个websocket请求返回True，如果是个普通的http请求返回False,可以用这个方法区分它们。

        2.request.websocket
        在一个websocket请求建立之后，这个请求将会有一个websocket属性，用来给客户端提供一个简单的api通讯，如果request.is_websocket()是False，这个属性将是None。

        3.WebSocket.wait()
        返回一个客户端发送的信息，在客户端关闭连接之前他不会返回任何值，这种情况下，方法将返回None

        4.WebSocket.read()
         如果没有从客户端接收到新的消息，read方法会返回一个新的消息，如果没有，就不返回。这是一个替代wait的非阻塞方法

        5.WebSocket.count_messages()
         返回消息队列数量

        6.WebSocket.has_messages()
         如果有新消息返回True，否则返回False

        7.WebSocket.send(message)
         向客户端发送消息

        8.WebSocket.__iter__()
         websocket迭代器




