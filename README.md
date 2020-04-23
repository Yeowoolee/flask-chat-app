# flask-chat-app
heroku : https://flask-chat-socketio.herokuapp.com/

> Goal

Flask, MongoDB Atlas, Socket.IO를 사용해 실시간 채팅 애플리케이션을 제작하고 배포하는 것을 목표로 합니다.

### 1\. Flask에서 Socket.IO 사용하기

> 서버 >> 클라이언트

Flask에서 Socket.IO를 사용하기 위해서 flask-socketio 라이브러리를 설치했습니다.

\>pip install flask-socketio

```
from flask_socketio import SocketIO, send
socketio = SocketIO(app)
```

라이브러리 사용을 위해 위와 같이 불러왔습니다. 

```
send(send_msg, broadcast=True)
```

send는 클라이언트에서 받아온 메시지를 다시 클라이언트에 전달합니다.

다수의 사용자가 실시간 채팅을 하기 위해 모든 메시지는 서버를 거쳐서 표시됩니다.

> 클라이언트 >> 서버

Socket.IO 사용을 위해 CDN 방식으로 불러왔고 jquery를 사용했습니다.

```
<script type='text/javascript' src='https://cdnjs.cloudflare.com/ajax/libs/socket.io/2.3.0/socket.io.js'></script>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/2.2.4/jquery.min.js"></script>
    
```

서버에 socket 전달을 위해 socket을 만들고 send 메서드를 사용해서 서버에 socket을 전달했습니다.

아래 코드는 socket.on('connect') 이므로 클라이언트가 소켓에 접근했을 때 보내지게 되는 메시지입니다.

```
$(document).ready(function() {
        const socket = io();
        socket.on('connect', function(){
            socket.send('|-----유저접속-----')
        });
```

입력한 이이디와 내용을 서버에 전달하는 코드입니다.

아이디가 입력되지 않았다면 '익명' 아이디를 가지도록 했습니다.

서버로 전달 후 메시지가 입력될 input의 value를 공백으로 만들어주기 위해 초기화했습니다.

```
$('#myMessage').keypress(function(){
    if (event.key === "Enter") {
    	let send_Python = ''
    if($('#anonymous').val()){
        send_Python = `${$('#anonymous').val()}|${$('#myMessage').val()}`;
    }else{
        send_Python = `익명|${$('#myMessage').val()}`;
    }
    socket.send(send_Python);
    $('#myMessage').val('');
    }
});
```

서버로부터 message를 전달 받으면 아래 코드가 실행됩니다. 받아온 message는 msg매개변수로 사용했습니다.

```
socket.on('message', function(msg){});
```

### 2\. MongoDB Atlas 사용

MongoDB Atlas는 웹 기반 데이터베이스로 URI 주소로 간단하게 연동할 수 있어서 사용했습니다.

MongoDB Atlas 사용을 위해 MongoDB Atlas 가입 후 데이터베이스를 만들었습니다.

[https://www.mongodb.com/cloud/atlas/register](https://www.mongodb.com/cloud/atlas/register)

Flask에서 MongoDB Atlas를 사용하기 위해서 pymongo 라이브러리를 설치했습니다.

\>pip install pymongo

Flask app을 정의하고 MONGO\_URI를 입력했습니다.

```
app = Flask(__name__)
app.config['MONGO_URI'] = os.environ['MONGO_KEY']
mongo = PyMongo(app)
history = mongo.db.MSG_History
```

위 코드로 history 변수에 DB를 연결했습니다.

이제 history.insert\_one(), history.find(), history.remove({ }) 등의 명령어로 DB를 정의, 조작, 제어할 수 있습니다.

사용자가 다시 접속하는 경우 이전 채팅 내용을 볼 수 있도록 MongoDB Atlas 를 사용해 채팅 내용을 저장합니다. 

```
history.insert_one(db_data)
```

사용자가 페이지 접속 시 (@app.route('/') 일 때)

채팅 내용은 30개가 넘어가면 모든 내용을 삭제시켜 최대 30개까지 저장하도록 했습니다.

```
if history.count() > 30:
        history.remove({ })
```

messages 변수에 모든 메시지 데이터를 삽입하고 index.html로 messages라는 변수로 전달합니다.

```
messages = history.find()
    return render_template('index.html', messages=messages)
```

그리고 저장된 채팅 데이터는 jinja문을 사용해서 클라이언트에게 표시되도록 했습니다.

```
{% for msg in messages %}           
      <li class="list-group-item d-flex justify-content-between align-items-center">
           <strong>{{msg.name}}</strong> {{msg.text}}
           <span class="badge badge-primary">[{{msg.get_time}}]</span>
      </li>
{% endfor %}
```

### 3\. Heroku 배포시 주의사항

> eventlet 설치

**\>pip install eventlet**

Socket.IO를 사용하기 위해 eventlet 사용이 권장됩니다.

> Procfile 변경

**web: gunicorn --worker-class eventlet -w 1 main:app**
