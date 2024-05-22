from flask import Flask, jsonify, request
from flask_socketio import SocketIO
from flask_cors import CORS

app = Flask(__name__)
socketio = SocketIO(app)
CORS(app)

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')


@app.route('/post-data', methods=['POST'])
def post_data():
    if request.is_json:
        data = request.get_json()  # Get data posted as JSON

        # Emitting to all connected clients (other servers)
        socketio.emit('run-js', {'code': data['code']})

        return jsonify({"message": "Data received, command sent to other servers"}), 200
    else:
        return jsonify({"error": "Request must be JSON"}), 400


@socketio.on('connect')
def handle_connect():
    print('Client connected')


if __name__ == "__main__":
    socketio.run(app, host='127.0.0.1', port=5000) 
