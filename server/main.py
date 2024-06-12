from flask import Flask, request, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow CORS for all routes
socketio = SocketIO(app, cors_allowed_origins="*")  # Allow CORS for Socket.IO

@app.route('/run-js', methods=['POST'])
def post_data():
    data = request.get_json()
    code = data.get('code')

    if code:
        socketio.emit('run-js', code)
        return jsonify({"response": "posted (200)"}), 200
    else:
        return jsonify({"error": "parse err (400)"}), 400

# Audio relay: gui -> viz
@socketio.on('audio-feed')
def handle_audio_request():
    socketio.emit('audio-feed')

# Audio relay: viz -> gui
@socketio.on('audio-feed-reply')
def handle_audio_reply(msg):
    socketio.emit('audio-feed-reply', msg)

# update vizualizer code
@socketio.on('run-js')
def handle_message(msg):
    socketio.emit('run-js', msg)


if __name__ == "__main__":
    socketio.run(app, host='127.0.0.1', port=5000, allow_unsafe_werkzeug=True) 

