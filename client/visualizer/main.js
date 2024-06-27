const { app, BrowserWindow } = require('electron');
const path = require('path');
const { spawn } = require('child_process');
const { checkForUpdates } = require('./update-scripts');

async function createWindow () {
    // Start the backend server
    const python = spawn('python', [path.join(__dirname, '/../../server', 'main.py')]);

    python.on('close', (code) => {
        console.log(`child process exited with code ${code}`);
    });

    // Load the viz window
    const win = new BrowserWindow({
        width: 800,
        height: 485,
        webPreferences: {
            preload: path.join(__dirname,'renderer.js'),  // Use 'preload' if this is a preload script
            nodeIntegration: true,
            contextIsolation: false
        },
    });

		// await checkForUpdates(); // Check for updates before creating the window

    win.loadFile(path.join(__dirname, 'index.html'));
};

app.whenReady().then(() => {
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

