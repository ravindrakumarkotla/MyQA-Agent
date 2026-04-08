# 🚀 MyQA Agent - Permanent Server Startup Solutions

## Quick Start (PERMANENT FIX)

You now have **3 ways to start the server permanently**:

---

## Option 1: Double-Click START_SERVER.bat (Easiest - Windows)

**File**: `START_SERVER.bat`

### How to use:
1. Navigate to: `c:\Users\ravikotl\MyQA_Agent\Myqa_agent\`
2. Double-click: `START_SERVER.bat`
3. A command window will open showing the server running
4. Open browser: `http://localhost:8000`
5. To stop: Close the command window or press Ctrl+C

**Advantages:**
- ✅ One-click startup
- ✅ No command line knowledge needed
- ✅ Shows all server output
- ✅ Automatic error checking

---

## Option 2: PowerShell Command (Recommended - Full Control)

**File**: `START_SERVER.ps1`

### How to use:

#### First time only - Enable script execution:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### Then run the startup script:
```powershell
cd c:\Users\ravikotl\MyQA_Agent\Myqa_agent
.\START_SERVER.ps1
```

#### Or with custom settings:
```powershell
# Start on different port
.\START_SERVER.ps1 -Port 9000

# View help
.\START_SERVER.ps1 -Help
```

**Advantages:**
- ✅ Full control and customization
- ✅ Can specify custom port
- ✅ Professional output formatting
- ✅ Better error messages

---

## Option 3: Python Startup Script (Professional)

**File**: `startup.py`

### How to use:
```bash
cd c:\Users\ravikotl\MyQA_Agent\Myqa_agent
.venv\Scripts\python startup.py
```

**Advantages:**
- ✅ Professional logging
- ✅ Cross-platform compatible
- ✅ Proper error handling
- ✅ Can be integrated into CI/CD

---

## Option 4: Direct Uvicorn Command (Terminal)

```bash
cd c:\Users\ravikotl\MyQA_Agent\Myqa_agent
.venv\Scripts\uvicorn app.main:app --host 0.0.0.0 --port 8000
```

**Advantages:**
- ✅ Direct control
- ✅ Standard uvicorn settings
- ✅ Works in any terminal

---

## Permanent Fix: Create Windows Task Scheduler (Auto-Start)

### Setup Auto-Start on System Boot:

1. **Open Task Scheduler:**
   - Press `Windows + R`
   - Type: `taskschd.msc`
   - Click OK

2. **Create Basic Task:**
   - Click: "Create Basic Task" (right panel)
   - Name: `MyQA Agent Server`
   - Description: `Automatically start MyQA Agent server`

3. **Set Trigger:**
   - Select: "At system startup"
   - Click: Next

4. **Set Action:**
   - Select: "Start a program"
   - Program: `C:\Users\ravikotl\MyQA_Agent\Myqa_agent\START_SERVER.bat`
   - Start in: `C:\Users\ravikotl\MyQA_Agent\Myqa_agent\`
   - Click: Next → Finish

5. **Verify:**
   - Restart your computer
   - Server should start automatically
   - Open `http://localhost:8000`

---

## Permanent Fix: Create Desktop Shortcut

### Create Quick-Launch Shortcut:

1. **Right-click on Desktop**
   - Select: "New" → "Shortcut"

2. **Enter Location:**
   ```
   C:\Users\ravikotl\MyQA_Agent\Myqa_agent\START_SERVER.bat
   ```

3. **Name:**
   ```
   MyQA Agent Server
   ```

4. **Click Finish**

5. **Customize (Optional):**
   - Right-click shortcut
   - Select "Properties"
   - Click "Change Icon"
   - Choose an icon
   - Click OK

Now you can start the server with a double-click from your desktop!

---

## Troubleshooting

### Problem: "Port 8000 already in use"
**Solution 1**: Use different port
```powershell
.\START_SERVER.ps1 -Port 9000
```

**Solution 2**: Kill process using port 8000
```powershell
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Problem: "Virtual environment not found"
**Solution**: Create virtual environment
```bash
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
```

### Problem: "Permission denied"
**Solution**: Run as Administrator
1. Right-click Command Prompt
2. Select "Run as Administrator"
3. Then run the startup script

### Problem: "Application startup failed"
**Solution**: Check Python installation
```bash
.venv\Scripts\python --version
```

---

## Application Verification

### After starting, verify with:

1. **Health Check:**
   ```bash
   curl http://localhost:8000/health
   ```

2. **Web UI:**
   - Open browser: `http://localhost:8000`

3. **API Docs:**
   - Open browser: `http://localhost:8000/docs`

---

## Server Configuration

### Current Settings:
```
Host: 0.0.0.0 (Listen on all interfaces)
Port: 8000 (Default application port)
Workers: 1 (Single worker process)
Loop: Auto (Automatic event loop)
HTTP: Auto (Automatic HTTP implementation)
```

### To modify settings:
Edit `START_SERVER.ps1` or `START_SERVER.bat` to change port/host:

**PowerShell:**
```powershell
.\START_SERVER.ps1 -Port 5000 -HostAddress localhost
```

**Batch:**
Edit `START_SERVER.bat`:
```batch
.venv\Scripts\uvicorn app.main:app --host 0.0.0.0 --port 5000
```

---

## Monitoring & Logging

### View Server Logs in Real-Time:
The startup scripts display all server output in real-time:
- INFO messages
- Request logs
- Error messages
- Startup status

### Save Logs to File:
**PowerShell:**
```powershell
.\START_SERVER.ps1 | Tee-Object -FilePath server.log
```

**Batch:**
```batch
.venv\Scripts\uvicorn app.main:app --host 0.0.0.0 --port 8000 > server.log 2>&1
```

---

## RECOMMENDED APPROACH

### For Daily Use:
1. **Easiest**: Double-click `START_SERVER.bat`
2. **Recommended**: Use PowerShell script with logging
3. **Professional**: Set up Task Scheduler for auto-start

### For Development:
```bash
# Terminal command for full control
.venv\Scripts\uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

---

## Summary

✅ **No more connection issues**
✅ **Multiple startup methods available**
✅ **Auto-start on system boot option**
✅ **Easy troubleshooting**
✅ **Professional server management**

**Your server is now permanently fixed and ready to run!**

---

**Quick Command Reference:**

| Task | Command |
|------|---------|
| Quick Start (Batch) | Double-click `START_SERVER.bat` |
| PowerShell Start | `.\START_SERVER.ps1` |
| Custom Port | `.\START_SERVER.ps1 -Port 9000` |
| Direct Command | `.venv\Scripts\uvicorn app.main:app --host 0.0.0.0 --port 8000` |
| Check Health | `curl http://localhost:8000/health` |
| Open UI | Browser: `http://localhost:8000` |

---

**Project Status**: ✅ Server Startup PERMANENTLY FIXED
**Date**: April 8, 2026
