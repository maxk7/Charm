const { app, BrowserWindow } = require('electron');
const express = require('express');
const http = require('http');
const socketIo = require('socket.io');

// Create the Express app
const expressApp = express();

// Create a server based on the Express app
const server = http.createServer(expressApp);

// Set up Socket.IO with CORS enabled
const io = socketIo(server, {
    cors: {
        origin: "*",  // Adjust this as necessary for your app
        methods: ["GET", "POST"]
    }
});

const path = require('path');
const { spawn } = require('child_process')

const createWindow = () => {
    const win = new BrowserWindow({
        width: 800,
        height: 485,
        webPreferences: {
            renderer: path.join(__dirname, 'client/renderer.js'),
        },
    });

    win.loadFile('client/index.html');

};

app.whenReady().then(() => {
    spawn("python", ["./flask_server/server/main.py"])
    createWindow();

    app.on('activate', () => {
        if (BrowserWindow.getAllWindows().length === 0) {
            createWindow();
        }
    });
});

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});
