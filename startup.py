#!/usr/bin/env python
"""
MyQA Agent - Startup Manager
Ensures the application always runs with proper error handling and recovery
"""

import subprocess
import sys
import time
import os
from pathlib import Path

def get_project_root():
    """Get the project root directory"""
    return Path(__file__).parent

def start_server():
    """Start the Uvicorn server with proper configuration"""
    project_root = get_project_root()
    venv_python = project_root / ".venv" / "Scripts" / "python.exe"
    
    if not venv_python.exists():
        print("❌ Error: Virtual environment not found")
        print(f"   Expected path: {venv_python}")
        sys.exit(1)
    
    # Server configuration
    host = "0.0.0.0"
    port = 8000
    
    print("=" * 70)
    print("🚀 MyQA Agent - Application Startup")
    print("=" * 70)
    print(f"📁 Project Root: {project_root}")
    print(f"🐍 Python Executable: {venv_python}")
    print(f"🌐 Server: http://0.0.0.0:{port}")
    print(f"⏰ Started at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    print()
    
    # Uvicorn command with optimized settings
    cmd = [
        str(venv_python),
        "-m",
        "uvicorn",
        "app.main:app",
        f"--host={host}",
        f"--port={port}",
        "--workers=1",
        "--loop=auto",
        "--http=auto"
    ]
    
    try:
        print(f"📋 Command: {' '.join(cmd)}\n")
        process = subprocess.Popen(
            cmd,
            cwd=str(project_root),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        
        print("📡 Server Output:")
        print("-" * 70)
        
        # Read output in real-time
        for line in process.stdout:
            print(line.rstrip())
        
        # Wait for process to complete
        process.wait()
        
    except KeyboardInterrupt:
        print("\n" + "=" * 70)
        print("⏹️  Server stopped by user")
        print("=" * 70)
        process.terminate()
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    start_server()
