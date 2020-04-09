import os
import time
from flask import Flask, render_template
from flask_socketio import SocketIO, send
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['APP_KEY']
app.config['MONGO_URI'] = os.environ['MONGO_KEY']
socketio = SocketIO(app, message_queue='redis://')
mongo = PyMongo(app)
history = mongo.db.MSG_History
@app.route('/')
def index():
    messages = history.find()
    return render_template('index.html', messages=messages)

@socketio.on('message')
def handleMessage(msg):
    now = time.localtime()
    get_time = "%04d/%02d/%02d %02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min)
    name, text = msg.split(" ")
    send_msg = f"{name} {text} [{get_time}]"
    db_data = {'name':name, 'text':text, 'get_time':get_time}
    history.insert_one(db_data)
    send(send_msg, broadcast=True)

if __name__ == '__main__':
    socketio.run(app)
