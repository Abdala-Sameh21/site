const express = require('express');
const http = require('http');
const { Server } = require('socket.io');
const { spawn } = require('child_process');
const path = require('path');

const app = express();
const server = http.createServer(app);
const io = new Server(server);

app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

const ADMIN_USER = "admin";
const ADMIN_PASS = "123456";

let runningProcess = null;

app.post('/api/login', (req, res) => {
    const { username, password } = req.body;
    if (username === ADMIN_USER && password === ADMIN_PASS) {
        res.json({ success: true });
    } else {
        res.status(401).json({ success: false, message: 'بيانات الدخول غير صحيحة' });
    }
});

io.on('connection', (socket) => {
    socket.on('start-script', () => {
        if (runningProcess) {
            socket.emit('output', '⚠️ السكربت قيد التشغيل بالفعل...\n');
            return;
        }

        socket.emit('output', '🚀 جاري تشغيل ملف Python الحقيقي...\n');

        // أمر تشغيل بايثون تلقائي حسب بيئة السيرفر
        const pythonCmd = process.platform === "win32" ? "python" : "python3";
        runningProcess = spawn(pythonCmd, ['-u', 'script.py']);

        runningProcess.stdout.on('data', (data) => {
            socket.emit('output', data.toString());
        });

        runningProcess.stderr.on('data', (data) => {
            socket.emit('output', `❌ [خطأ]: ${data.toString()}`);
        });

        runningProcess.on('close', (code) => {
            socket.emit('output', `\n🛑 تم انتهاء العملية (رمز الإغلاق: ${code})\n`);
            runningProcess = null;
        });
    });

    socket.on('stop-script', () => {
        if (runningProcess) {
            runningProcess.kill('SIGINT');
            runningProcess = null;
            socket.emit('output', '\n⚠️ تم إيقاف السكربت يدويًا.\n');
        } else {
            socket.emit('output', 'ℹ️ لا يوجد سكربت يعمل حالياً.\n');
        }
    });
});

const PORT = process.env.PORT || 3000;
server.listen(PORT, () => console.log(`Server running on port ${PORT}`));
