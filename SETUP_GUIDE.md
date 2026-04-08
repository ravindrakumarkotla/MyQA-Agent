# Detailed Setup and Run Guide for AI QA Agent

## Quick Start Guide

This guide provides step-by-step instructions to set up and run the AI QA Agent application.

### Prerequisites

- **Python 3.10 or higher** installed on your system
- **pip** (Python package manager)
- **git** (optional, for cloning the repository)
- Any text editor or IDE (VS Code, PyCharm, etc.)

### Step 1: Navigate to Project Directory

```powershell
# On Windows (PowerShell)
cd C:\Users\ravikotl\MyQA_Agent\Myqa_agent

# On macOS/Linux
cd /path/to/agentic-qa
```

### Step 2: Create Virtual Environment

Virtual environments isolate project dependencies and prevent conflicts with other projects.

```powershell
# Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Windows (Command Prompt)
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

**Note**: After activation, your prompt should show `(venv)` prefix.

### Step 3: Verify Python Installation

```powershell
python --version
# Should output: Python 3.10.x or higher

pip --version
# Should output: pip version
```

### Step 4: Upgrade pip

```powershell
# Windows, macOS, Linux
python -m pip install --upgrade pip
```

### Step 5: Install Dependencies

```powershell
pip install -r requirements.txt
```

**Expected output**: All packages should install without errors. This installs:
- FastAPI: Web framework
- Uvicorn: ASGI server
- Pydantic: Data validation
- PyPDF2: PDF parsing
- python-docx: DOCX parsing
- openpyxl: Excel export
- pandas: Data manipulation

### Step 6: Create `.env` File (Optional)

```powershell
# Copy the example environment file
Copy-Item .env.example .env

# Or create manually and add:
# LLM_API_KEY=your_api_key_if_available
# DEBUG=True
```

### Step 7: Verify Project Structure

```powershell
# View project structure
tree /F

# Or manually verify these directories exist:
# - app/
# - app/api/
# - app/services/
# - app/models/
# - app/utils/
# - uploads/
# - exports/
```

### Step 8: Run the Application

```powershell
# Development mode (with auto-reload)
uvicorn app.main:app --reload

# Or use the alternative command
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Production mode (without auto-reload)
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

**Expected output**:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

### Step 9: Verify Application is Running

In a new terminal window:

```powershell
# Check health
curl http://localhost:8000/health

# Or using PowerShell
Invoke-WebRequest http://localhost:8000/health
```

**Expected response**:
```json
{"status": "healthy", "service": "AI QA Agent API", "version": "1.0.0"}
```

### Step 10: Access API Documentation

Open your browser and navigate to:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Running Example Workflow

### 1. Create Sample Document

Create a file `sample_requirements.txt`:

```
User Story: Login System
As a user, I want to log in to my account with email and password.

Acceptance Criteria:
- Given I enter valid email and password, when I click login, then I should access my dashboard
- Given I enter invalid password, when I click login, then I should see an error message
- Given email field is empty, when I load the page, then the login button should be disabled

Preconditions:
- User has registered account
- User is on login page

Business Rules:
- Passwords must be minimum 8 characters
- Maximum 5 login attempts per hour
- Session expires after 30 minutes of inactivity

Constraints:
- Login must complete within 2 seconds
- Support 10,000 concurrent users
```

### 2. Upload Document

In a new PowerShell terminal:

```powershell
# Upload the document
$response = curl -X POST "http://localhost:8000/api/upload/document" `
  -F "file=@./sample_requirements.txt" | ConvertFrom-Json

$fileId = $response.file_id
Write-Host "Uploaded file ID: $fileId"
```

### 3. Analyze Document

```powershell
# Analyze the uploaded document
curl -X POST "http://localhost:8000/api/analyze/document" `
  -H "Content-Type: application/json" `
  -d "{`"file_id`": `"$fileId`"}"
```

### 4. Generate Test Cases

```powershell
# Generate 10 test cases
curl -X POST "http://localhost:8000/api/generate/test-cases" `
  -H "Content-Type: application/json" `
  -d "{`"file_id`": `"$fileId`", `"num_test_cases`": 10}"
```

### 5. Export to Word

```powershell
# Export to Word document
curl -X POST "http://localhost:8000/api/export/test-cases" `
  -H "Content-Type: application/json" `
  -d "{`"file_id`": `"$fileId`", `"format`": `"docx`"}" `
  -o "TestCases.docx"

Write-Host "Word document saved as TestCases.docx"
```

### 6. Export to Excel

```powershell
# Export to Excel spreadsheet
curl -X POST "http://localhost:8000/api/export/test-cases" `
  -H "Content-Type: application/json" `
  -d "{`"file_id`": `"$fileId`", `"format`": `"xlsx`"}" `
  -o "TestCases.xlsx"

Write-Host "Excel document saved as TestCases.xlsx"
```

## Deactivating Virtual Environment

When you're done working:

```powershell
# Windows
deactivate

# macOS/Linux
deactivate
```

## Troubleshooting

### Issue: "python command not found"

**Solution**: Ensure Python is installed and added to PATH
```powershell
# Check Python installation
python --version

# If not found, download from python.org and install
```

### Issue: "ModuleNotFoundError" on import

**Solution**: Ensure virtual environment is activated and dependencies are installed
```powershell
# Verify venv is activated (look for (venv) in prompt)
.\venv\Scripts\Activate.ps1

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: "Port 8000 already in use"

**Solution**: Use a different port
```powershell
uvicorn app.main:app --port 8001
```

### Issue: File upload fails

**Solution**: Ensure directories exist and are writable
```powershell
# Create directories if needed
New-Item -ItemType Directory -Force -Path "uploads"
New-Item -ItemType Directory -Force -Path "exports"

# Check permissions
Get-ChildItem -Attributes !D uploads
```

## Windows-Specific Notes

### Using Command Prompt Instead of PowerShell

```cmd
# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Run application
uvicorn app.main:app --reload
```

### Using Git Bash

```bash
# Create virtual environment
python -m venv venv
source venv/Scripts/activate

# Run application
uvicorn app.main:app --reload
```

## macOS/Linux Notes

### Install Python 3.10+

```bash
# macOS (using Homebrew)
brew install python@3.10

# Ubuntu/Debian
sudo apt-get install python3.10 python3.10-venv

# CentOS/RHEL
sudo yum install python310
```

### Run with Different Python Version

```bash
# Specify Python version when creating venv
python3.10 -m venv venv
source venv/bin/activate
```

## Next Steps

1. **Explore API Documentation**: Visit http://localhost:8000/docs
2. **Review Code Structure**: Check the app directory for implementation details
3. **Customize Functionality**: Modify services and utilities for your needs
4. **Integrate Real LLM**: Add your LLM API key to `app/services/ai_agent.py`
5. **Deploy Application**: Containerize with Docker or deploy to cloud platform

## Performance Tips

- **CPU**: Application uses minimal CPU for document parsing
- **Memory**: Mock AI responses use minimal memory (~50MB)
- **I/O**: Document parsing speed depends on file size and type
- **Network**: API responses typically < 1 second for file operations

## Production Deployment

Before deploying to production:

1. Set `DEBUG=False` in `.env`
2. Configure specific `CORS_ORIGINS` instead of `*`
3. Use production ASGI server (Gunicorn + Uvicorn)
4. Set up proper logging
5. Configure database for persistence
6. Set up authentication/authorization
7. Use environment-specific `.env` files
8. Configure reverse proxy (Nginx)
9. Enable HTTPS/SSL
10. Set up monitoring and alerting

Example production startup:

```bash
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker
```

## Getting Help

- Check API docs: http://localhost:8000/docs
- Review README.md for API examples
- Check app logs for error details
- Verify all dependencies are installed: `pip list`
- Ensure Python version is 3.10+: `python --version`

---

**Ready to start?** Run: `uvicorn app.main:app --reload`
