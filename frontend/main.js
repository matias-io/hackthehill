const { app, BrowserWindow, ipcMain, dialog } = require('electron');
const path = require('path');

let mainWindow;

app.on('ready', () => {
    mainWindow = new BrowserWindow({
        webPreferences: {
            contextIsolation: true,
            enableRemoteModule: false,
            preload: path.join(__dirname, 'preload.js'), // Ensure you have a preload script
        },
    });

    mainWindow.loadURL('http://localhost:3000'); // Your Next.js app URL
});

// Handle the file dialog IPC
ipcMain.handle('open-file-dialog', async () => {
    const result = await dialog.showOpenDialog(mainWindow, {
        properties: ['openFile']
    });
    
    return result.canceled ? null : result.filePaths[0]; // Return the file path
});


// const { app, BrowserWindow } = require('electron');

// const { ipcMain, dialog } = require('electron');

// ipcMain.handle('open-file-dialog', async () => {
//   const { canceled, filePaths } = await dialog.showOpenDialog({
//     properties: ['openFile'],
//   });
//   return canceled ? null : filePaths[0];
// });

// function createWindow () {
//   const win = new BrowserWindow({
//     width: 800,
//     height: 600,
//     webPreferences: {
//       nodeIntegration: true
//     }
//   })

//   win.loadURL('http://localhost:3000')
// }

// app.whenReady().then(createWindow)