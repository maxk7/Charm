document.addEventListener('DOMContentLoaded', () => {
	const socket = io("http://127.0.0.1:5000", {
    cors: {
        origin: "file://",
        methods: ["GET", "POST"]
    }
	});


	socket.on('connect', function() {
			console.log('Connected to server');
	});

	socket.on('server_message', function(data) {
			console.log(data.message);  // Logs 'Hello from server on connect!'
	});

	socket.on('run-js', function (data) {
			console.log('Received code to run:', data.code);
			try {
					eval(data.code); // Execute code in the Electron app
			} catch (error) {
					console.error('Error executing code:', error);
			}
	});

	socket.on('disconnect', function () {
			console.log('Disconnected');
	});
});
