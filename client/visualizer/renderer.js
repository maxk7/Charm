const io = require('socket.io-client');
document.addEventListener('DOMContentLoaded', () => {
	const socket = io("http://127.0.0.1:5000");

	socket.on('run-js', function (data) {
			console.log('Received code to run:', data);
			try {
					eval(data); // Execute code in the Electron app
			} catch (error) {
					console.error('Error executing code:', error);
			}
	});

	socket.on('audio-feed', function() {
		socket.emit('audio-feed-reply', a.fft);
	});
});
